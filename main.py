import requests
import rx
from rx import Observable, Observer


class MyObserver(Observer):
    def on_next(self, x):
        print("Got: %s" % x)

    def on_error(self, e):
        print("Got error: %s" % e)

    def on_completed(self):
        print("Sequence completed")

def weather(city):
    w = requests.get('http://api.openweathermap.org/data/2.5/weather?q={}'.format(city)).json()
    return w['main']['temp']/10

sensor = Observable.interval(30000).map(lambda d: weather('Kiev,UA')).retry().distinct_until_changed()
sensor.subscribe(MyObserver())
