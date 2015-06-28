from sensomatic.sources.utils import data_source


@data_source
class ReedSwitch5Events:
    """
    Raspberry Pi GPIO event provider from Reed Switch connected to pin 5 and GND.
    Port 5 sets up to use internal pull-up resistor.
    """
    PIN = 5
    provides = 'reed_switch_5'

    def __init__(self):
        import RPi.GPIO as GPIO
        self.GPIO = GPIO

        self.GPIO.setmode(self.GPIO.BOARD)
        self.GPIO.setup(self.PIN, self.GPIO.IN, pull_up_down=self.GPIO.PUD_UP)

    def __next__(self):
        return self.GPIO.input(self.PIN)

    def __iter__(self):
        return self
