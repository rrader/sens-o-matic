from sensomatic.sources.utils import data_source


@data_source
class FileContent:
    """
    Example of source. Provides file content for the file path specified in the constructor.
    """
    provides = 'file_content'

    def __init__(self, path):
        self.path = path

    def __next__(self):
        return open(self.path).read().strip()

    def __iter__(self):
        return self
