from rx import Observer
from sensomatic.sensors.weather import weather_sensor
import sensomatic.sources.defaults


class MyObserver(Observer):
    def on_next(self, x):
        print("Got: %s" % x)

    def on_error(self, e):
        print("Got error: %s" % e)

    def on_completed(self):
        print("Sequence completed")


weather_sensor['Kiev,UA'].subscribe(MyObserver())
