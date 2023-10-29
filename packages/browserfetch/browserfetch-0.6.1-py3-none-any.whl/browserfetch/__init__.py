__version__ = '0.6.1'

import atexit
from asyncio import CancelledError, Event, Task, get_running_loop, wait_for
from collections import defaultdict
from dataclasses import dataclass
from json import dumps, loads
from logging import getLogger
from typing import Any
from urllib.parse import urlencode

from aiohttp import ClientSession, ClientWebSocketResponse
from aiohttp.web import Application, RouteTableDef, WebSocketResponse
from aiohttp.web_runner import AppRunner, TCPSite

logger = getLogger(__name__)
# maps host to its host_ready event or its websocket
hosts: dict[
    str, Event | WebSocketResponse | ClientWebSocketResponse
] = defaultdict(Event)
# maps response event id to its response event or response dict
responses: dict[int, Event | dict] = {}


class BrowserError(Exception):
    pass


@dataclass(slots=True, weakref_slot=True)
class Response:
    """
    For the meaning of attributes see:
    https://developer.mozilla.org/en-US/docs/Web/API/Response
    """

    body: bytes
    ok: bool
    redirected: bool
    status: int
    status_text: str
    type: str
    url: str
    headers: dict

    def text(self, encoding=None, errors='strict') -> str:
        return self.body.decode(encoding or 'utf-8', errors)

    def json(self, encoding=None, errors='strict'):
        if encoding is None:
            return loads(self.body)
        return loads(self.text(encoding=encoding, errors=errors))


def extract_host(url: str) -> str:
    return url.partition('//')[2].partition('/')[0]


async def _response(
    data: dict,
    body: bytes | None,
    /,
) -> dict:
    host = data.pop('host', None) or extract_host(data['url'])
    response_ready = Event()
    event_id = id(response_ready)
    data['event_id'] = event_id
    responses[event_id] = response_ready

    bytes_ = dumps(data).encode()
    if body is not None:
        bytes_ += b'\0' + body

    ws = hosts[host]
    if isinstance(ws, Event):
        await ws.wait()
        ws = hosts[host]

    await ws.send_bytes(bytes_)

    try:
        await wait_for(response_ready.wait(), data['timeout'])
    except TimeoutError:
        responses.pop(event_id, None)
        raise

    return responses.pop(event_id)


async def receive_responses(ws: WebSocketResponse | ClientWebSocketResponse):
    while True:
        blob = await ws.receive_bytes()
        json_blob, _, body = blob.partition(b'\0')
        j = loads(json_blob)
        j['body'] = body
        event_id = j.pop('event_id')
        try:
            event = responses[event_id]
        except KeyError:  # lock has reached timeout already
            continue
        responses[event_id] = j
        event.set()


routes = RouteTableDef()


@routes.get('/ws')
async def _(request):
    ws = WebSocketResponse()
    await ws.prepare(request)

    host = await ws.receive_str()
    logger.info('registering host %s', host)

    ws_or_e = hosts[host]
    hosts[host] = ws
    if isinstance(ws_or_e, Event):
        ws_or_e.set()

    try:
        await receive_responses(ws)
    except TypeError:
        logger.info('host WebSocket was closed')
        hosts[host] = Event()


@routes.get('/relay')
async def _(request):
    ws = WebSocketResponse()
    await ws.prepare(request)

    while True:
        try:
            bytes_ = await ws.receive_bytes()
        except TypeError:  # ws closed
            return
        data, null, body = bytes_.partition(b'\0')
        data = loads(data)
        relay_event_id = data['event_id']

        try:
            # just to pop the event from responses
            r = await _response(data, body if null else None)
        except TimeoutError:
            r = {'error': 'TimeoutError in relay'}

        r['event_id'] = relay_event_id
        body = r.pop('body')
        await ws.send_bytes(dumps(r).encode() + b'\0' + body)


async def relay_client(server_host, server_port):
    async with ClientSession() as session:
        relay_url = f'ws://{server_host}:{server_port}/relay'
        async with session.ws_connect(relay_url) as ws:
            logger.info('connected to %s', relay_url)
            hosts.default_factory = lambda: ws
            for host, ws_or_e in hosts.items():
                hosts[host] = ws
                if isinstance(ws_or_e, Event):
                    ws_or_e.set()
            try:
                await receive_responses(ws)
            except TypeError:
                logger.info('relay server WebSocket was closed')
                return


async def fetch(
    url: str,
    *,
    params: dict = None,
    body: bytes = None,
    timeout: int | float = 95,
    options: dict = None,
    host=None,
) -> Response:
    """Fetch using browser fetch API available on host.

    :param url: the URL of the resource you want to fetch.
    :param params: parameters to be url-encoded and added to url.
    :param body: the body of the request (do not add to options).
    :param timeout: timeout in seconds (do not add to options).
    :param options: See https://developer.mozilla.org/en-US/docs/Web/API/fetch
    :param host: `location.host` of the tab that is supposed to handle this
        request.
    :return: a dict of response values.
    """
    if params is not None:
        url += urlencode(params)

    d = await _response(
        {
            'host': host,
            'url': url,
            'options': options,
            'timeout': timeout,
        },
        body,
    )

    if (err := d.get('error')) is not None:
        raise BrowserError(err)

    return Response(**d)


async def get(
    url: str,
    *,
    params: dict = None,
    options: dict = None,
    host: str = None,
    timeout: int | float = 95,
) -> Response:
    if options is None:
        options = {'method': 'GET'}
    else:
        options['method'] = 'GET'
    return await fetch(
        url, options=options, host=host, timeout=timeout, params=params
    )


async def post(
    url: str,
    *,
    params: dict = None,
    body: bytes = None,
    data: dict = None,
    json=None,
    timeout: int | float = 95,
    options: dict = None,
    host: str = None,
) -> Response:
    if options is None:
        options: dict[str, Any] = {'method': 'POST'}
    else:
        options['method'] = 'POST'

    if json is not None:
        assert body is None
        body = dumps(json).encode()
        headers = options.setdefault('headers', {})
        headers['Content-Type'] = 'application/json'

    if data is not None:
        assert body is None
        body = urlencode(data).encode()
        headers = options.setdefault('headers', {})
        headers['Content-Type'] = 'application/x-www-form-urlencoded'

    return await fetch(
        url,
        options=options,
        host=host,
        timeout=timeout,
        body=body,
        params=params,
    )


app = Application()
app.add_routes(routes)
app_runner = AppRunner(app)


def shutdown_server(loop):
    logger.info('waiting for app_runner.cleanup()')
    loop.run_until_complete(app_runner.cleanup())


def shutdown_relay_client(loop, task: Task):
    task.cancel()
    try:
        loop.run_until_complete(task)
    except CancelledError:
        pass


async def start_server(*, host='127.0.0.1', port=9404):
    loop = get_running_loop()
    await app_runner.setup()
    site = TCPSite(app_runner, host, port)
    try:
        await site.start()  # does not block
    except OSError as e:
        logger.info(
            'port %d is in use; will try to connect to existing server; %r',
            port,
            e,
        )
        relay_task = loop.create_task(relay_client(host, port))
        atexit.register(shutdown_relay_client, loop, relay_task)
    else:
        atexit.register(shutdown_server, loop)
        logger.info('server started at http://%s:%s', host, port)
