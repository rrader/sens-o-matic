"""
Simple sensor example that generates events based on UAH currency change.
"""

from rx import Observable
from sensomatic.sources.utils import get_source

__all__ = ['reed_switch_sensor']


source = get_source("reed_switch_5")()
reed_switch_sensor =\
    Observable.from_iterable(source)
