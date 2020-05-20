from ..base import CRUDAPI

__all__ = [
    'CurrencyAPI',
]


class CurrencyAPI(CRUDAPI):
    """Currency API."""

    def update(self, data, **kw):
        raise NotImplementedError()

    def get(self, identifier, **kw):
        raise NotImplementedError()
