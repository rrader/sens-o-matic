SOURCES_REGISTRY = {}
DEFAULT_IMPLEMENTATIONS = {}


def data_source(cls):
    """
    Decorator for Source classes. Registers them in the global SOURCES_REGISTRY
    Source class should have 'provides' field
    :param cls: source class
    :return: same class
    """
    SOURCES_REGISTRY.setdefault(cls.provides, [])
    SOURCES_REGISTRY[cls.provides].append(cls)
    return cls


def set_default(cls):
    """
    Using set_default you can set default source for some kind of sources
    mentioned in the 'provides' field.
    :param cls: source class you want to be default between it's kind of sources
    """
    DEFAULT_IMPLEMENTATIONS[cls.provides] = cls


class MissingRequiredDefaultSource(Exception):
    """
    This exception will be raised if you didn't set default source for sources kind.
    Maybe you didn't import defaults?
    >>> import sensomatic.sources.examples.defaults
    """
    pass


def get_source(provides):
    """
    Returns default source class for needed kind of sources
    :param provides: kind of sources
    :return: source class
    """
    if provides not in DEFAULT_IMPLEMENTATIONS:
        raise MissingRequiredDefaultSource()
    return DEFAULT_IMPLEMENTATIONS[provides]
