import requests
from sensomatic.sources.utils import data_source, set_default


@data_source
class OpenWeatherMapTemperature:
    provides = 'temperature_for_city'

    def __init__(self, city):
        self.city = city

    def __next__(self):
        w = requests.get('http://api.openweathermap.org/data/2.5/weather?q={}'.format(self.city)).json()
        return w['main']['temp']/10

    def __iter__(self):
        return self
