from rx import Observable
from rx.internal import extensionclassmethod


@extensionclassmethod(Observable)
def from_iterable_with_interval(cls, period, iterable, scheduler=None):
    """
    Creates an Observable that polls iterator made from iterable every period millis.
    :param period: polling interval
    :param iterable: data source provider.
    :return: Observable instance
    """
    iterator = iter(iterable)
    return Observable.interval(period, scheduler=scheduler).map(lambda v: next(iterator))
