"""
More complex sensor example, it's sensor factory for different cities.
"""

from rx import Observable
from sensomatic.rxutils.scheduler import aio_scheduler
from sensomatic.sources.utils import get_source

__all__ = ['weather_sensor']


MINUTES_5 = 5 * 60 * 1000


class WebTemperatureSensor:
    """
    Sensor factory provides Observable singleton objects for every city.
    It has dict-like interface, e.g. to get temperature in the Kiev,UA
    you can do
    >>> weather_sensor['Kiev,UA'].subscribe(...)
    Every time you'll get same Observable object
    >>> weather_sensor['Kiev,UA']) == weather_sensor['Kiev,UA'])  ->  True
    """
    def __init__(self):
        self.sensors = {}

    def __getitem__(self, item):
        if item not in self.sensors:
            source = get_source('temperature_for_city')(item)
            self.sensors[item] = self.create(source)
        return self.sensors[item]

    def create(self, source):
        return Observable.\
            from_iterable_with_interval(MINUTES_5, source, scheduler=aio_scheduler).\
            retry().\
            distinct_until_changed()


weather_sensor = WebTemperatureSensor()
