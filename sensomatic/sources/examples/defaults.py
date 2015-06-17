"""
Sets up default implementations for sensors.
To use it just import it in your project
>>> import sensomatic.sources.examples.defaults
or make your own list.
"""

from sensomatic.sources.examples import OpenWeatherMapTemperature
from sensomatic.sources.examples import UAHCurrencies
from sensomatic.sources.utils import set_default

set_default(OpenWeatherMapTemperature)
set_default(UAHCurrencies)
