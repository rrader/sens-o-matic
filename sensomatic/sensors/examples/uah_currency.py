"""
Simple sensor example that generates events based on UAH currency change.
"""

from rx import Observable
from sensomatic.sources.utils import get_source

__all__ = ['weather_sensor']


MINUTES_10 = 10 * 60 * 1000
source = get_source("uah_currencies")
uah_currency_sensor =\
    Observable.from_iterable_with_interval(MINUTES_10, source).\
    retry().\
    distinct_until_changed()
