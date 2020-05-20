from ..base import BaseAPI, check_token
from ...exceptions import RecommendAPIError

__all__ = [
    'CatalogUploadAPI',
]


class CatalogUploadAPI(BaseAPI):
    """Catalog Upload API."""

    @check_token
    def get(self, identifier, **kw):
        r"""
        Return details of an upload by identifier.

        :param identifier: identifier of object (required).
        :param \**kw: additional keyword arguments are passed to requests.

        :raises: :class:`recommendpy.exceptions.RecommendAPIError`.

        :return: result of response.json().
        """
        return self._client.send(
            'get', self.get_path(identifier=identifier), **kw
        )

    @check_token
    def simple_list_batch(self, data, **kw):
        r"""
        Upload catalog simple batch data.

        :param data: data to upload (required).
        :param \**kw: additional keyword arguments are passed to requests.

        :raises: :class:`recommendpy.exceptions.RecommendAPIError`.

        :return: result of response.json().
        """
        return self._client.send(
            'post', self.get_path(method='list_batch'), **kw
        )

    @check_token
    def simple_product_batch(self, data, **kw):
        r"""
        Upload catalog simple batch data.

        :param data: data to upload (required).
        :param \**kw: additional keyword arguments are passed to requests.

        :raises: :class:`recommendpy.exceptions.RecommendAPIError`.

        :return: result of response.json().
        """
        return self._client.send(
            'post', self.get_path(method='product_batch'), **kw
        )

    @check_token
    def simple_variation_batch(self, data, **kw):
        r"""
        Upload catalog simple batch data.

        :param data: data to upload (required).
        :param \**kw: additional keyword arguments are passed to requests.

        :raises: :class:`recommendpy.exceptions.RecommendAPIError`.

        :return: result of response.json().
        """
        return self._client.send(
            'post', self.get_path(method='variation_batch'), **kw
        )

    @check_token
    def __call__(self, mode, level_mode, level_store_code=None, **kw):
        r"""
        Initialize catalog upload.

        :param mode: mode (required).
            One of ['block', 'append', 'append_by_timestamp'].
        :param level_mode: level mode (required). One of ['account', 'store'].
        :param level_store_code: level store code
            (used for level_mode == 'store'). Defaults to ``None``.
        :param \**kw: additional keyword arguments are passed to requests.

        :raises: :class:`recommendpy.exceptions.RecommendAPIError`.

        :return: result of response.json().
        """
        if mode not in ['block', 'append', 'append_by_timestamp']:
            raise RecommendAPIError('Incorrect mode.')
        if level_mode not in ['account', 'store']:
            raise RecommendAPIError('Incorrect level_mode.')
        data = {
            'mode': mode,
            'level': {
                'mode': level_mode,
            }
        }
        if level_mode == 'store':
            data['level']['store_code'] = level_store_code

        return self._client.send(
            'post', self.get_path(), data, **kw
        )

    @check_token
    def list_batch(self, identifier, data, **kw):
        r"""
        Upload catalog batch data.

        :param identifier: Identifier of upload ID (required).
        :param data: data to upload (required).
        :param \**kw: additional keyword arguments are passed to requests.

        :raises: :class:`recommendpy.exceptions.RecommendAPIError`.

        :return: result of response.json().
        """
        if not identifier:
            raise RecommendAPIError('Incorrect identifier.')
        return self._client.send(
            'post', self.get_path(identifier=identifier, method='list_batch'),
            **kw
        )

    @check_token
    def product_batch(self, identifier, data, **kw):
        r"""
        Upload catalog batch data.

        :param identifier: Identifier of upload ID (required).
        :param data: data to upload (required).
        :param \**kw: additional keyword arguments are passed to requests.

        :raises: :class:`recommendpy.exceptions.RecommendAPIError`.

        :return: result of response.json().
        """
        if not identifier:
            raise RecommendAPIError('Incorrect identifier.')
        return self._client.send(
            'post', self.get_path(
                identifier=identifier, method='product_batch'
            ),
            **kw
        )

    @check_token
    def variation_batch(self, identifier, data, **kw):
        r"""
        Upload catalog batch data.

        :param identifier: Identifier of upload ID (required).
        :param data: data to upload (required).
        :param \**kw: additional keyword arguments are passed to requests.

        :raises: :class:`recommendpy.exceptions.RecommendAPIError`.

        :return: result of response.json().
        """
        if not identifier:
            raise RecommendAPIError('Incorrect identifier.')
        return self._client.send(
            'post', self.get_path(
                identifier=identifier, method='variation_batch'
            ),
            **kw
        )

    @check_token
    def commit(self, identifier, **kw):
        r"""
        Mark catalog upload as successful and complete it.

        :param identifier: Identifier of upload ID (required).
        :param \**kw: additional keyword arguments are passed to requests.

        :raises: :class:`recommendpy.exceptions.RecommendAPIError`.

        :return: result of response.json().
        """
        return self._client.send(
            'post', self.get_path(
                identifier=identifier, method='commit'
            ),
            **kw
        )

    @check_token
    def rollback(self, identifier, **kw):
        r"""
        Mark catalog upload as unsuccessful and rollback it.

        :param identifier: Identifier of upload ID (required).
        :param \**kw: additional keyword arguments are passed to requests.

        :raises: :class:`recommendpy.exceptions.RecommendAPIError`.

        :return: result of response.json().
        """
        return self._client.send(
            'post', self.get_path(
                identifier=identifier, method='commit'
            ),
            **kw
        )
