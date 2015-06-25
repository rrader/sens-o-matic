# from rx import Observer
# from sensomatic.sources import defaults
# from sensomatic.sensors.reed_switch import reed_switch_sensor
#
#
# class MyObserver(Observer):
#     def on_next(self, x):
#         print("Got: %s" % x)
#
#     def on_error(self, e):
#         print("Got error: %s" % e)
#
#     def on_completed(self):
#         print("Sequence completed")
#
#
# # weather_sensor['Kiev,UA'].subscribe(MyObserver())
# reed_switch_sensor.subscribe(MyObserver())
import asyncio
from sensomatic.ui.server import Server


def main():
    server = Server()

    loop = asyncio.get_event_loop()
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.finalize()
    loop.close()


if __name__ == "__main__":
    main()
