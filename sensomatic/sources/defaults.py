"""
Sets up default implementations for sensors.
To use it just import it in your project
>>> import sensomatic.sources.defaults
or make your own list.
"""

from sensomatic.sources import OpenWeatherMapTemperature
from sensomatic.sources.utils import set_default

set_default(OpenWeatherMapTemperature)
