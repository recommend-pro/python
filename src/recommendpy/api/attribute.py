from .base import BaseAPI, CRUDAPI, check_token
from ..exceptions import RecommendAPIError

__all__ = [
    'AttributeAPI',
    'AttributeStoreMappingAPI'
]

ATTRIBUTE_TYPES = [
    'list', 'product', 'variation', 'order', 'order_item', 'contact'
]


class AttributeAPI(CRUDAPI):
    """Attribute API."""

    def __init__(self, client, endpoint, entity_type):
        r"""
        Initialize AttributeAPI object.

        :param client: :class:`recommendpy.RecommendAPI` object (required).
        :param endpoint: string path for api endpoint (required).
        :param entity_type: Identifier of entity type (required).
            One of [list, product, variation, order, order_item, contact].

        :raises: :class:`recommendpy.exceptions.RecommendAPIError`
            if incorrect entity_type.
        """
        if entity_type not in ATTRIBUTE_TYPES:
            raise RecommendAPIError('Invalid parameter entity_type')
        self._client = client
        self.endpoint = endpoint.format(entity_type=entity_type)


class AttributeStoreMappingAPI(BaseAPI):
    """Attribute Store Mapping API."""

    def __init__(self, client, endpoint, entity_type, attribute_code):
        r"""
        Initialize AttributeStoreMappingAPI object.

        :param client: :class:`recommendpy.RecommendAPI` object (required).
        :param endpoint: string path for api endpoint (required).
        :param entity_type: Identifier of entity type (required).
            One of [list, product, variation, order, order_item, contact].
        :param attribute_code: Identifier of attribute (required).

        :raises: :class:`recommendpy.exceptions.RecommendAPIError`
            if incorrect entity_type.
        """
        if entity_type not in ATTRIBUTE_TYPES:
            raise RecommendAPIError('Invalid parameter entity_type')
        self._client = client
        self.endpoint = endpoint
        self.entity_type = entity_type
        self.attribute_code = attribute_code

    def get_path(self, identifier):
        r"""
        Get relative path.

        :param identifier: identifier of store (required).
        :return: the formatted string of self.endpoint with entity_type,
            attribute_code and store_code parameters.
        """
        return self.endpoint.format(
            entity_type=self.entity_type,
            attribute_code=self.attribute_code,
            store_code=identifier
        )

    @check_token
    def get(self, identifier, **kw):
        r"""
        Return attribute mapping for store.

        :param identifier: identifier of store (required).
        :param \**kw: additional keyword arguments are passed to requests.

        :raises: :class:`recommendpy.exceptions.RecommendAPIError`.

        :return: result of response.json().
        """
        return self._client.send(
            'get', self.get_path(identifier), **kw
        )

    @check_token
    def create(self, identifier, data, **kw):
        r"""
        Create attribute mapping for store.

        :param identifier: identifier of store (required).
        :param data: data for request (required).
        :param \**kw: additional keyword arguments are passed to requests.

        :raises: :class:`recommendpy.exceptions.RecommendAPIError`.

        :return: result of response.json().
        """
        return self._client.send(
            'post', self.get_path(identifier), data, **kw
        )

    @check_token
    def delete(self, identifier, **kw):
        r"""
        Delete attribute mapping for store.

        :param identifier: identifier of store (required).
        :param \**kw: additional keyword arguments are passed to requests.

        :raises: :class:`recommendpy.exceptions.RecommendAPIError`.

        :return: result of response.json().
        """
        return self._client.send(
            'delete', self.get_path(identifier), **kw
        )
