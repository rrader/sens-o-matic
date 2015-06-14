SOURCES_REGISTRY = {}
DEFAULT_IMPLEMENTATIONS = {}


def data_source(cls):
    SOURCES_REGISTRY.setdefault(cls.provides, [])
    SOURCES_REGISTRY[cls.provides].append(cls)
    return cls


def set_default(cls):
    DEFAULT_IMPLEMENTATIONS[cls.provides] = cls


class MissingRequiredDefaultSource(Exception):
    pass


def get_source(provides):
    if provides not in DEFAULT_IMPLEMENTATIONS:
        raise MissingRequiredDefaultSource()
    return DEFAULT_IMPLEMENTATIONS[provides]
