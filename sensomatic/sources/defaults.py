"""
Sets up default implementations for sensors.
To use it just import it in your project
>>> import sensomatic.sources.defaults
or make your own list.
"""

from sensomatic.sources.gpio import ReedSwitchEvents
from sensomatic.sources.weather import OpenWeatherMapTemperature
from sensomatic.sources.uah_currency import UAHCurrencies
from sensomatic.sources.utils import set_default


set_default(OpenWeatherMapTemperature)
set_default(UAHCurrencies)
set_default(ReedSwitchEvents)
