from rx import Observable
from sensomatic.sources.utils import get_source

__all__ = ['weather_sensor']


MINUTES_5 = 5 * 60 * 1000


class WeatherSensor:
    def __init__(self):
        self.sensors = {}

    def __getitem__(self, item):
        if item not in self.sensors:
            source = get_source('temperature_for_city')(item)
            self.sensors[item] = self.create(source)
        return self.sensors[item]

    def create(self, source):
        return Observable.from_iterable_with_interval(MINUTES_5, source).retry().distinct_until_changed()


weather_sensor = WeatherSensor()
