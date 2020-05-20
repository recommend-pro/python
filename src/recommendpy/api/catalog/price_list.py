from ..base import CRUDAPI

__all__ = [
    'PriceListAPI',
]


class PriceListAPI(CRUDAPI):
    """Price list API."""

    def update(self, data, **kw):
        raise NotImplementedError()
