import asyncio
import json
import logging
from aiohttp import web
import aiohttp
from rx import Observer
from sensomatic.ui.persistence.models import Sensor, get_last_record
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
    def __init__(self, sensor_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sensor_name = sensor_name
        self.queue = asyncio.Queue()
        self.last_record = get_last_record(sensor_name)
        logger.debug("AIOQueueObserver created")

    def on_next(self, new_value):
        if self.last_record and str(self.last_record.value) == str(new_value.value):
            logger.warning("value {} for sensor '{}' was duplicated (happens every time new listener connected). "
                           "Not sending to WS.".format(new_value.value, self.sensor_name))
            return
        logger.debug("value {} arrived".format(new_value))
        asyncio.async(self.queue.put(new_value))
        logger.debug("value is in the queue!")
        self.last_record = new_value

        if self.queue.qsize() > AUTODISPOSING_QUEUE_SIZE_THRESHOLD:
            logger.info("queue size is growing, guess that reader was disconnected. disposing observer.")
            self.dispose()

    def on_error(self, e):
        logger.error("Got error: {}".format(e))


def value_to_json(value, sensor_name):
    return {
              'sensorName': sensor_name,
              'value': value.value,
              'timestamp': value.timestamp.isoformat()
    }


@aiohttp_class_handler
class DataStreamHandler:
    @asyncio.coroutine
    def handle(self, request):
        ws = web.WebSocketResponse()
        ws.start(request)


        msg = yield from ws.receive()
        request = json.loads(msg.data)
        sensor_name = request['sensorName']

        self.assert_first_request_is_subscribe(request, ws)
        sensor_meta = self.get_sensor_metadata(request, ws)
        sensor = sensor_meta['factory']()

        observer = AIOQueueObserver(sensor_name)
        sensor.subscribe(observer)
        logger.info("new listener registered for '{}'".format(sensor_name))

        history = [value_to_json(value, sensor_name) for value
                   in Sensor.select().
                   where(Sensor.name == sensor_name).
                   order_by(Sensor.timestamp.desc()).
                   limit(5)
                   ]
        history = list(reversed(history))

        ws.send_str(json.dumps({'$type': 'subscribedOK', 'sensorName': sensor_name,
                                'sensorStaticData': sensor_meta['meta'],
                                'history': history}))

        while True:
            logger.debug("waiting for the new value")
            value = yield from observer.queue.get()
            logger.info("sending new value to WS")

            json_value = value_to_json(value, sensor_name)
            json_value.update({'$type': 'dataReceived'})

            ws.send_str(json.dumps(json_value))

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
