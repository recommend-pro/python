from .base import BaseAPI, CRUDAPI, check_token

__all__ = [
    'ConfigAPI',
    'StoreAPI',
    'WebhookAPI',
]

# TODO: build account


class ConfigAPI(BaseAPI):
    """Config API."""

    @check_token
    def __call__(self, **kw):
        r"""
        Return account config.

        :param \**kw: additional keyword arguments are passed to requests.

        :raises: :class:`recommendpy.exceptions.RecommendAPIError`.

        :return: result of response.json().
        """
        return self._client.send(
            'get', self.get_path(), **kw
        )

    @check_token
    def update(
        self, default_store, default_currency, default_price_list,
        **kw
    ):
        r"""
        Update config.

        :param default_store: default store (required).
        :param default_currency: default currency (required).
        :param default_price_list: default price list (required).
        :param \**kw: additional keyword arguments are passed to requests.

        :raises: :class:`recommendpy.exceptions.RecommendAPIError`.

        :return: result of response.json().
        """
        data = {
            'default_store': default_store,
            'default_currency': default_currency,
            'default_price_list': default_price_list,
        }
        return self._client.send(
            'put', self.get_path(), data, **kw
        )


class StoreAPI(CRUDAPI):
    """Store API."""

    pass


class WebhookAPI(CRUDAPI):
    """WebhookAPI API."""

    def update(self, identifier, **kw):
        raise NotImplementedError()
