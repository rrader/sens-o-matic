import logging
from rx import Observer
from sensomatic.ui.persistence.models import Sensor, get_last_record
from sensomatic.ui.sensors_config import KNOWN_SENSORS


logger = logging.getLogger('persistence')


class PersistenceObserver(Observer):
    """
    Observes the sensor new values and stores them into the database
    """
    def __init__(self, sensor_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sensor_name = sensor_name
        logger.debug("PersistenceObserver for sensor '{}' created".format(sensor_name))

    def on_next(self, new_value):
        last_record = get_last_record(self.sensor_name)
        if last_record and str(last_record.value) == str(new_value.value):
            logger.warning("value {} for sensor '{}' was duplicated (maybe server was restarted). Not saving to DB.".
                           format(new_value.value, self.sensor_name))
            return
        Sensor.create(name=self.sensor_name, value=str(new_value.value), timestamp=new_value.timestamp)
        logger.debug("new value {} for '{}' saved to DB".format(new_value.value, self.sensor_name))

    def on_error(self, e):
        logger.error("Got error: {}".format(e))


def configure_persistence(sensors_list=[]):
    for sensor_name in sensors_list:
        sensor = KNOWN_SENSORS[sensor_name]['factory'] ()
        observer = PersistenceObserver(sensor_name)
        sensor.subscribe(observer)
        logger.debug("persistence configured for {}".format(sensor_name))
