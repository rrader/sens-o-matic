"""
Simple sensor example that generates events based on file content change.
"""
from rx import Observable
from sensomatic.rxutils.scheduler import aio_scheduler
from sensomatic.sources.utils import get_source

__all__ = ['file_content_sensor']

class FileContentSensor:
    """
    Sensor factory provides Observable singleton objects for every file path.
    It has dict-like interface, e.g. to get sensor for file '/tmp/test_file'
    you can do
    >>> file_content_sensor['/tmp/test_file'].subscribe(...)
    Every time you'll get same Observable object
    >>> file_content_sensor['/tmp/test_file']) == file_content_sensor['/tmp/test_file'])  ->  True
    """
    def __init__(self):
        self.sensors = {}

    def __getitem__(self, path):
        if path not in self.sensors:
            source = get_source('file_content')(path)
            self.sensors[path] = self.create(source)
        return self.sensors[path]

    def create(self, source):
        return Observable.\
            from_iterable_with_interval(500, source, scheduler=aio_scheduler).\
            distinct_until_changed().\
            timestamp()

file_content_sensor = FileContentSensor()
