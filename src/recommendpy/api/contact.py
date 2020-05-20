from .base import BaseAPI, CRUDAPI, check_token

from ..exceptions import RecommendAPIError


__all__ = [
    'ContactAPI',
    'ContactBatchAPI',
    'ContactSegmentAPI',
    'ContactListAPI',
]


class ContactAPI(BaseAPI):
    """Contact API."""

    @check_token
    def search(self, emails=None, customer_ids=None, **kw):
        r"""
        Search data of contact by specified field(s).

        :param emails: list of emails. Defaults to ``None``.
        :param customer_ids: list of customer_ids. Defaults to ``None``.
        :param \**kw: additional keyword arguments are passed to requests.

        :raises: :class:`recommendpy.exceptions.RecommendAPIError`.

        :return: result of response.json().
        """
        # TODO: skip parameter
        if not emails and not customer_ids:
            raise RecommendAPIError('Please send emails or customer_ids')
        data = {}
        if emails:
            data['emails'] = emails
        if customer_ids:
            data['customer_ids'] = customer_ids

        return self._client.send(
            'post', self.get_path(method='search'), **kw
        )


class ContactBatchAPI(BaseAPI):
    """Contact batch API."""

    @check_token
    def customer_id(self, data, **kw):
        r"""
        Create batch of contacts.

        :param data: data for request (required).
        :param \**kw: additional keyword arguments are passed to requests.

        :raises: :class:`recommendpy.exceptions.RecommendAPIError`.

        :return: result of response.json().
        """
        return self._client.send(
            'post', self.get_path(method='customer_id'), data
        )

    @check_token
    def email(self, data, **kw):
        r"""
        Create batch of contacts.

        :param data: data for request (required).
        :param \**kw: additional keyword arguments are passed to requests.

        :raises: :class:`recommendpy.exceptions.RecommendAPIError`.

        :return: result of response.json().
        """
        return self._client.send(
            'post', self.get_path(method='email'), data
        )


class ContactSegmentAPI(BaseAPI):
    """Contact segment API."""

    @check_token
    def __call__(self, **kw):
        r"""
        Return segments.

        :param \**kw: additional keyword arguments are passed to requests.

        :raises: :class:`recommendpy.exceptions.RecommendAPIError`.

        :return: result of response.json().
        """
        return self._client.send(
            'get', self.get_path(), **kw
        )


class ContactListAPI(CRUDAPI):
    """Contact list API."""

    @check_token
    def attach(
        self, identifier, customer_ids=None, emails=None, push_tokens=None,
        **kw
    ):
        r"""
        Attach contacts to contact list by identifier.

        :param identifier: identifier of contact list (required).
        :param customer_ids: list of customer_ids. Defaults to ``None``.
        :param emails: list of emails. Defaults to ``None``.
        :param push_tokens: list of push_tokens. Defaults to ``None``.
        :param \**kw: additional keyword arguments are passed to requests.

        :raises: :class:`recommendpy.exceptions.RecommendAPIError`.

        :return: result of response.json().
        """
        if not emails and not customer_ids and not push_tokens:
            raise RecommendAPIError(
                'Please send emails, customer_ids or push_tokens'
            )
        data = {}
        if emails:
            data['emails'] = emails
        if customer_ids:
            data['customer_ids'] = customer_ids
        if push_tokens:
            data['push_tokens'] = push_tokens
        return self._client.send(
            'post', self.get_path(identifier=identifier, method='attach'),
            data=data
        )

    @check_token
    def detach(
        self, identifier, customer_ids=None, emails=None, push_tokens=None,
        **kw
    ):
        r"""
        Detach contacts from contact list by identifier.

        :param identifier: identifier of contact list (required).
        :param customer_ids: list of customer_ids. Defaults to ``None``.
        :param emails: list of emails. Defaults to ``None``.
        :param push_tokens: list of push_tokens. Defaults to ``None``.
        :param \**kw: additional keyword arguments are passed to requests.

        :raises: :class:`recommendpy.exceptions.RecommendAPIError`.

        :return: result of response.json().
        """
        if not emails and not customer_ids and not push_tokens:
            raise RecommendAPIError(
                'Please send emails, customer_ids or push_tokens'
            )
        data = {}
        if emails:
            data['emails'] = emails
        if customer_ids:
            data['customer_ids'] = customer_ids
        if push_tokens:
            data['push_tokens'] = push_tokens
        return self._client.send(
            'post', self.get_path(identifier=identifier, method='detach')
        )

    @check_token
    def clean(self, identifier, **kw):
        r"""
        Clean contacts from contact list by identifier.

        :param identifier: identifier of contact list (required).
        :param \**kw: additional keyword arguments are passed to requests.

        :raises: :class:`recommendpy.exceptions.RecommendAPIError`.

        :return: result of response.json().
        """
        return self._client.send(
            'post', self.get_path(identifier=identifier, method='detach')
        )
