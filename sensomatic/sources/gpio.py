from time import sleep
from sensomatic.sources.utils import data_source
import RPi.GPIO as GPIO

PIN = 5


@data_source
class ReedSwitchEvents:
    """
    Raspberry Pi GPIO event provider from Reed Switch connected to pin 5 and GND.
    Port 5 sets up to use internal pull-up resistor.
    """
    provides = 'reed_switch_5'

    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def __next__(self):
        value = GPIO.input(PIN)
        while True:
            new_value = GPIO.input(PIN)
            if value != new_value:
                return new_value
            sleep(0.5)

    def __iter__(self):
        return self
