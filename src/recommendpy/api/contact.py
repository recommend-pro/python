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
    def search(
        self, emails=None, customer_ids=None, list_code=None, skip=None,
        limit=None, **kw
    ):
        r"""
        Search data of contact by specified field(s).

        :param emails: list of emails. Defaults to ``None``.
        :param customer_ids: list of customer_ids. Defaults to ``None``.
        :param list_code: identifier of contact list. Defaults to ``None``.
        :param skip: skip documents. Defaults to ``None``.
        :param limit: Limit documents. Defaults to ``None``.
        :param \**kw: additional keyword arguments are passed to requests.

        :raises: :class:`recommendpy.exceptions.RecommendAPIError`.

        :return: result of response.json().
        """
        data = {}
        params = {}
        if emails:
            data['emails'] = emails
        if customer_ids:
            data['customer_ids'] = customer_ids
        if list_code:
            data['list_code'] = list_code
        if skip:
            params['skip'] = skip
        if params:
            params['limit'] = limit

        return self._client.send(
            'post', self.get_path(method='search'), data=data, params=params,
            **kw
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


class ContactSegmentAPI(CRUDAPI):
    """Contact segment API."""

    _test_data = {
        'title': 'test_title'
    }

    @check_token
    def search(
        self, identifier, field=None, identifiers=None, skip=None, limit=None,
        **kw
    ):
        r"""
        Search data of contact segment.

        :param identifier: identifier of contact segment (required).
        :param field: name of field to match by identifiers (required).
            One of ['customer_id', 'email']
        :param identifiers: list of identifiers (required).
        :param customer_ids: list of customer_ids. Defaults to ``None``.
        :param list_code: identifier of contact list. Defaults to ``None``.
        :param skip: skip documents. Defaults to ``None``.
        :param limit: Limit documents. Defaults to ``None``.
        :param \**kw: additional keyword arguments are passed to requests.

        :raises: :class:`recommendpy.exceptions.RecommendAPIError`.

        :return: result of response.json().
        """
        data = {}
        params = {}

        if field and field not in ['customer_id', 'email']:
            raise RecommendAPIError(
                'Please send valid `field`'
            )

        if field:
            data['field'] = field
        if skip:
            params['skip'] = skip
        if params:
            params['limit'] = limit

        return self._client.send(
            'post', self.get_path(
                identifier=identifier, custom=['identifiers', 'search']
            ),
            data=data, params=params, **kw
        )

    @check_token
    def attach(self, identifier, field, identifiers, **kw):
        r"""
        Attach identifiers to contact segment by specified identifier.

        :param identifier: identifier of contact segment (required).
        :param field: name of field to match by identifiers (required).
            One of ['customer_id', 'email']
        :param identifiers: list of identifiers (required).
        :param \**kw: additional keyword arguments are passed to requests.

        :raises: :class:`recommendpy.exceptions.RecommendAPIError`.

        :return: result of response.json().
        """
        if field not in ['customer_id', 'email']:
            raise RecommendAPIError(
                'Please send valid `field`'
            )
        data = {
            'field': field,
            'identifiers': identifiers,
        }
        return self._client.send(
            'post', self.get_path(identifier=identifier, method='attach'),
            data=data
        )

    @check_token
    def detach(self, identifier, field, identifiers, **kw):
        r"""
        Detach contacts from contact list by identifier.

        :param identifier: identifier of contact segment (required).
        :param field: name of field to match by identifiers (required).
            One of ['customer_id', 'email']
        :param identifiers: list of identifiers (required).
        :param \**kw: additional keyword arguments are passed to requests.

        :raises: :class:`recommendpy.exceptions.RecommendAPIError`.

        :return: result of response.json().
        """
        if field not in ['customer_id', 'email']:
            raise RecommendAPIError(
                'Please send valid `field`'
            )
        data = {
            'field': field,
            'identifiers': identifiers,
        }
        return self._client.send(
            'post', self.get_path(identifier=identifier, method='detach'),
            data=data
        )


class ContactListAPI(CRUDAPI):
    """Contact list API."""

    _test_data = {
        'title': 'test_title'
    }

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
            'post', self.get_path(identifier=identifier, method='detach'),
            data=data
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
