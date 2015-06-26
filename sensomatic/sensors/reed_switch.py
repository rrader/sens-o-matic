"""
Simple sensor example that generates events based on UAH currency change.
"""
from rx import Observable
from sensomatic.rxutils.scheduler import aio_scheduler
from sensomatic.sources.utils import get_source

__all__ = ['reed_switch_sensor']

source = get_source("reed_switch_5")()
reed_switch_sensor = \
    Observable.from_iterable_with_interval(500, source, scheduler=aio_scheduler). \
    distinct_until_changed(). \
    timestamp()
