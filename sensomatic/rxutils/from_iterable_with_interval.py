from rx import Observable
from rx.internal import extensionclassmethod


@extensionclassmethod(Observable)
def from_iterable_with_interval(cls, period, iterable, scheduler=None):
    iterator = iter(iterable)
    return Observable.interval(period, scheduler=scheduler).map(lambda v: next(iterator))
