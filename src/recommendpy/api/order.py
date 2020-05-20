from .base import CRUDAPI, check_token

__all__ = [
    'OrderAPI',
]


class OrderAPI(CRUDAPI):
    """Order API."""

    def list(self, **kw):
        raise NotImplementedError()

    @check_token
    def batch(self, data, **kw):
        r"""
        Create batch of orders.

        :param data: data for request (required).
        :param \**kw: additional keyword arguments are passed to requests.

        :raises: :class:`recommendpy.exceptions.RecommendAPIError`.

        :return: result of response.json().
        """
        return self._client.send(
            'post', self.get_path(method='batch'),
            data=data
        )
