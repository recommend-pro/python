from ..base import CRUDAPI

__all__ = [
    'EnvironmentAPI',
]


class EnvironmentAPI(CRUDAPI):
    """Environment API."""

    def update(self, data, **kw):
        raise NotImplementedError()

    def get(self, identifier, **kw):
        raise NotImplementedError()
