from sensomatic.sources.utils import data_source
import RPi.GPIO as GPIO


@data_source
class ReedSwitch5Events:
    """
    Raspberry Pi GPIO event provider from Reed Switch connected to pin 5 and GND.
    Port 5 sets up to use internal pull-up resistor.
    """
    PIN = 5
    provides = 'reed_switch_5'

    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def __next__(self):
        return GPIO.input(self.PIN)
        # while True:
        #     new_value = GPIO.input(PIN)
        #     if value != new_value:
        #         return new_value
        #     sleep(0.5)

    def __iter__(self):
        return self
