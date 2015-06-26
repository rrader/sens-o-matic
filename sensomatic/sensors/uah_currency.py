"""
Simple sensor example that generates events based on UAH currency change.
"""

from rx import Observable
from sensomatic.sources.utils import get_source
from sensomatic.rxutils.scheduler import aio_scheduler

__all__ = ['uah_currency_sensor']


MINUTES_1 = 60 * 1000
source = get_source("uah_currencies")()
uah_currency_sensor =\
    Observable.from_iterable_with_interval(MINUTES_1, source, scheduler=aio_scheduler).\
    retry().\
    distinct_until_changed()
