import asyncio
import json
import logging
import os
import threading
from aiohttp import web
from rx import Observer
from sensomatic.sources import defaults
from sensomatic.sensors.reed_switch import reed_switch_sensor


class GPIOObserver(Observer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(">>>> ", threading.current_thread().name)
        self.queue = asyncio.Queue()
        logging.debug("GPIOObserver created")

    def on_next(self, new_value):
        print(">>>> ", threading.current_thread().name)
        logging.debug("value {} arrived".format(new_value))
        asyncio.async(self.queue.put(new_value))
        logging.info("value is in the queue!")

    def on_error(self, e):
        logging.error("Got error: {}".format(e))


class Server:
    def __init__(self):
        self.app = self.create_app()
        self.handler = self.app.make_handler()
        self.srv = self.create_http_server()

    @asyncio.coroutine
    def hello(self, request):
        return web.Response(body=b"Hello, world")

    @asyncio.coroutine
    def websocket_handler(self, request):
        ws = web.WebSocketResponse()
        ws.start(request)

        msg = yield from ws.receive()
        request = json.loads(msg.data)
        if request['$type'] != 'subscribe':
            ws.send_str(
                json.dumps({
                    '$type': 'error',
                    'message': 'First request should have "subscribe" type'
                })
            )
            ws.close()
        if request['sensorName'] not in ['door']:
            ws.send_str(
                json.dumps({
                    '$type': 'error',
                    'message': 'sensorName "{}" not found'.format(request['sensorName'])
                })
            )
            ws.close()
        # observer = GPIOObserver(loop=asyncio.get_event_loop())
        observer = GPIOObserver()
        reed_switch_sensor.subscribe(observer)
        logging.info("new listener registered")
        ws.send_str(json.dumps({'$type': 'subscribedOK', 'sensorName': request['sensorName']}))

        while True:
            logging.info("waiting for the new value")
            value = yield from observer.queue.get()
            logging.info("sending new value to WS")
            ws.send_str(json.dumps(
                {
                    '$type': 'dataReceived',
                    'sensorName': request['sensorName'],
                    'value': value.value,
                    'timestamp': value.timestamp.isoformat()
                })
            )

        return ws

    def create_app(self):
        app = web.Application()
        app.router.add_route('GET', '/', self.hello)
        app.router.add_route('GET', '/updates', self.websocket_handler)
        app.router.add_static('/ui',
                              os.path.join(os.path.dirname(__file__), 'static'),
                              name='static')
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

