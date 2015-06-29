import asyncio
import json
import logging
from aiohttp import web
import aiohttp
from rx import Observer
from sensomatic.ui.sensors_config import KNOWN_SENSORS

AUTODISPOSING_QUEUE_SIZE_THRESHOLD = 5

logger = logging.getLogger('WS')


def aiohttp_class_handler(cls):
    @asyncio.coroutine
    def handler_coroutine(request):
        handler = cls()
        response = yield from handler.handle(request)
        return response
    return handler_coroutine


class AIOQueueObserver(Observer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queue = asyncio.Queue()
        logger.debug("AIOQueueObserver created")

    def on_next(self, new_value):
        logger.debug("value {} arrived".format(new_value))
        asyncio.async(self.queue.put(new_value))
        logger.debug("value is in the queue!")

        if self.queue.qsize() > AUTODISPOSING_QUEUE_SIZE_THRESHOLD:
            logger.info("queue size is growing, guess that reader was disconnected. disposing observer.")
            self.dispose()

    def on_error(self, e):
        logger.error("Got error: {}".format(e))


@aiohttp_class_handler
class DataStreamHandler:
    @asyncio.coroutine
    def handle(self, request):
        ws = web.WebSocketResponse(autoclose=False)
        ws.start(request)

        msg = yield from ws.receive()
        request = json.loads(msg.data)
        self.assert_first_request_is_subscribe(request, ws)
        sensor_meta = self.get_sensor_metadata(request, ws)
        sensor = sensor_meta['factory']()

        observer = AIOQueueObserver()
        sensor.subscribe(observer)
        logger.info("new listener registered for '{}'".format(request['sensorName']))
        ws.send_str(json.dumps({'$type': 'subscribedOK', 'sensorName': request['sensorName'],
                                'sensorStaticData': sensor_meta['meta']}))

        while True:
            logger.debug("waiting for the new value")
            value = yield from observer.queue.get()
            logger.info("sending new value to WS")
            ws.send_str(json.dumps(
                {
                    '$type': 'dataReceived',
                    'sensorName': request['sensorName'],
                    'value': value.value,
                    'timestamp': value.timestamp.isoformat()
                })
            )
            msg = yield from ws.receive()
            if msg.tp == aiohttp.MsgType.close:
                break

        return ws

    def get_sensor_metadata(self, request, ws):
        if request['sensorName'] not in KNOWN_SENSORS.keys():
            ws.send_str(
                json.dumps({
                    '$type': 'error',
                    'message': 'sensorName "{}" not found'.format(request['sensorName'])
                })
            )
            ws.close()
        return KNOWN_SENSORS[request['sensorName']]

    def assert_first_request_is_subscribe(self, request, ws):
        if request['$type'] != 'subscribe':
            ws.send_str(
                json.dumps({
                    '$type': 'error',
                    'message': 'First request should have "subscribe" type'
                })
            )
            ws.close()
