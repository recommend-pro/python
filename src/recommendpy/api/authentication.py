from .base import BaseAPI

from ..exceptions import RecommendAuthenticationError

__all__ = [
    'AuthenticateAPI',
]


class AuthenticateAPI(BaseAPI):
    """Authenticate API."""

    def __call__(self, api_key, **kw):
        r"""
        Return JWT tokens.

        :param api_key: api_key (required).
        :param \**kw: additional keyword arguments are passed to requests.

        :raises: :class:`recommendpy.exceptions.RecommendAPIError`.

        :return: result of response.json().
        """
        return self._client.send(
            'post', self.get_path(), {'key': api_key}, **kw
        )

    def refresh(self, refresh_token=None, update_refresh_token=False, **kw):
        r"""
        Refresh JWT tokens.

        :param refresh_token: refresh token. Defaults to ``None``.
        :param update_refresh_token: updates refresh token.
            Defaults to ``False``.
        :param \**kw: additional keyword arguments are passed to requests.

        :raises: :class:`recommendpy.exceptions.RecommendAPIError`.
        :raises: :class:`recommendpy.exceptions.RecommendAuthenticationError`
            if refresh token is expired.

        :return: result of response.json().
        """
        refresh_token = refresh_token or self._client.get_token('refresh')
        if not refresh_token or refresh_token.is_expired:
            raise RecommendAuthenticationError('Invalid refresh token.')
        return self._client.send(
            'post', self.get_path(method='refresh'), {
                'refresh_token': refresh_token.token,
                'update_refresh_token': update_refresh_token
            }, **kw
        )
