import asyncio
from aiohttp import web

from sensomatic.sources import defaults
from sensomatic.ui.data_stream import DataStreamHandler
from sensomatic.ui.static_utils import static_handler


class Server:
    def __init__(self):
        self.app = self.create_app()
        self.handler = self.app.make_handler()
        self.srv = self.create_http_server()

    def create_app(self):
        app = web.Application()
        app.router.add_route('GET', '/updates', DataStreamHandler)
        app.router.add_route('GET', '/ui/{path:.*}', static_handler)
        return app

    def create_http_server(self):
        loop = asyncio.get_event_loop()
        srv = loop.run_until_complete(
            loop.create_server(self.handler, '0.0.0.0', 8080)
        )
        print('will be serving on', srv.sockets[0].getsockname())
        return srv

    def finalize(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.handler.finish_connections(1.0))
        self.srv.close()
        loop.run_until_complete(self.srv.wait_closed())
        loop.run_until_complete(self.app.finish())
