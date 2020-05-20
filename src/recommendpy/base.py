import requests

import json

from .exceptions import (
    RecommendAPIError,
    RecommendBatchErrorList,
    RecommendNotFoundError,
    RecommendUnauthorizedError,
    RecommendAuthenticationError,
    RecommendTokenError,
)

from .api import (
    AuthenticateAPI,
    ContactAPI,
    ContactBatchAPI,
    ContactSegmentAPI,
    ContactListAPI,
    MessagingAPI,
    MessagingChannelBatchAPI,
    MessagingChannelEmailAPI,
    OrderAPI,
    ConfigAPI,
    StoreAPI,
    WebhookAPI,
    AttributeAPI,
    AttributeStoreMappingAPI,
    CurrencyAPI,
    EnvironmentAPI,
    PriceListAPI,
    CatalogUploadAPI,
)

from .token import RecommendAPIToken

import logging
log = logging.getLogger(__name__)


class RecommendAPI(object):
    tokens = {}
    is_auth_token_setted = False

    def __init__(
        self, account_id, api_url='https://api.recommend.pro/v3',
        auth_token=None, get_token_func=None, set_token_func=None,
        credential_file_path=None
    ):
        self.api_url = api_url
        self.account_id = account_id
        self.get_token_func = get_token_func
        self.set_token_func = set_token_func
        self.credential_file_path = credential_file_path

        self._session = requests.Session()
        self._session.headers.update({
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        })
        if auth_token:
            self.set_auth_token(auth_token)
        self.map_apis()

    def set_auth_token(self, token=None):
        if not token:
            token = self.get_token('auth')
        self.tokens['auth'] = token

        self.is_auth_token_setted = True
        self._session.headers.update({
            'Authorization': 'Bearer {}'.format(token.token),
        })

    def service_url(self, name):
        return '{api_url}/{account_id}/{service}'.format(
            api_url=self.api_url,
            account_id=self.account_id,
            service=name,
        )

    def get_token(self, token_type, try_to_load=True):
        if self.get_token_func:
            return self.get_token_func(token_type)
        try:
            return self.tokens[token_type]
        except KeyError:
            if try_to_load:
                self.load_tokens()
                return self.get_token(token_type, False)
        return None

    def load_tokens(self):
        if not self.credential_file_path:
            raise RecommendTokenError('Credential file path is invalid')
        try:
            with open(self.credential_file_path, 'r') as f:
                data = json.load(f)
                for k, v in data.items():
                    token = RecommendAPIToken()
                    token.set_from_dict(v, True)
                    self.tokens[k] = token
        except OSError:  # NOQA
            pass
        except json.JSONDecodeError as e:
            raise RecommendTokenError(str(e))

    def set_token(self, token_type, token):
        if self.set_token_func:
            return self.set_token_func(token_type, token)
        self.load_tokens()

        self.tokens[token_type] = token

        with open(self.credential_file_path, 'w') as f:
            data = {k: v.to_dict() for k, v in self.tokens.items()}
            json.dump(data, f)

    def update_tokens(self, data, update_refresh_token=True):
        if data.get('result'):
            data = data['result']

        token_types = ['auth']
        if update_refresh_token:
            token_types.append('refresh')
        for token_type in token_types:
            if not data.get(token_type):
                raise RecommendAuthenticationError(
                    'Unable to get {token_type} token'.format(
                        token_type=token_type.capitalize()
                    )
                )
            token = RecommendAPIToken()
            try:
                token.set_from_dict(data[token_type])
            except Exception as e:
                raise RecommendAuthenticationError(str(e))

            self.set_token(token_type, token)

    def _authenticate(self, key):
        self.update_tokens(self.authenticate(key))

    def refresh_token(self, update_refresh_token=False):
        self.update_tokens(
            self.authenticate.refresh(
                update_refresh_token=update_refresh_token
            ),
            update_refresh_token=update_refresh_token
        )

    def send(self, method, name, data=None, raw=False, **args):
        # args = {}
        if data:
            args['data'] = json.dumps(data)

        response = getattr(self._session, method)(
            self.service_url(name),
            verify=False,
            **args
        )

        if raw:
            log.debug(
                'Request: {method}:{name}:{args}.\n Response: {response}.'
                .format(method=method, name=name, args=args, response=response)
            )
            return response

        try:
            data = response.json()
            log.debug(
                'Request: {method}:{name}:{args}.\n Response: {data}.'
                .format(method=method, name=name, args=args, data=data)
            )
        except json.JSONDecodeError:
            log.debug(
                'Request: {method}:{name}:{args}.\n Response: {response}.'
                .format(method=method, name=name, args=args, response=response)
            )
            raise RecommendAPIError(response=response)

        if response.status_code == 404:
            raise RecommendNotFoundError(response=response)
        elif response.status_code == 401:
            raise RecommendUnauthorizedError(response=response)
        if response.status_code >= 400:
            raise RecommendAPIError(response=response)

        if not data:
            raise RecommendAPIError(response=response)

        try:
            if data and data['success']:  # asbool(data['success']):
                return data
        except KeyError:
            pass

        if data.get('batch_error_list'):
            raise RecommendBatchErrorList(response=response)

        try:
            if data and data['error_message']:
                raise RecommendAPIError(
                    message=data['error_message'],
                    response=response
                )
        except (TypeError, KeyError):
            pass

        raise RecommendAPIError(response=response)

    def map_apis(self):
        # Access and Authentication API
        self.authenticate = AuthenticateAPI(self, 'authenticate')

        # Contact API
        self.contact = ContactAPI(self, 'contact')
        self.contact.batch = ContactBatchAPI(self, 'contact/batch')
        self.contact.segment = ContactSegmentAPI(self, 'contact/segment')
        self.contact.list = ContactListAPI(self, 'contact/list')

        # Messaging API
        self.messaging = MessagingAPI(self, 'messaging')
        self.messaging.channel_batch = MessagingChannelBatchAPI(
            self, 'messaging/channel/batch'
        )
        self.messaging.channel_email = MessagingChannelEmailAPI(
            self, 'messaging/channel/email'
        )

        # Order API
        self.order = OrderAPI(self, 'order')

        # Core API
        self.config = ConfigAPI(self, 'config')
        self.store = StoreAPI(self, 'store')
        self.webhook = WebhookAPI(self, 'webhook')

        # Attribute API
        self.attribute = lambda entity_type: AttributeAPI(
            self, 'attribute/{entity_type}', entity_type=entity_type
        )
        self.attribute_store_mapping = lambda entity_type, attribute_code: \
            AttributeStoreMappingAPI(
                self,
                'attribute/{entity_type}/{attribute_code}'
                '/store/{store_code}/mapping',
                entity_type=entity_type,
                attribute_code=attribute_code
            )

        # Catalog API
        self.currency = CurrencyAPI(self, 'currency')
        self.environment = EnvironmentAPI(self, 'environment')
        self.price_list = PriceListAPI(self, 'price_list')
        self.catalog_upload = CatalogUploadAPI(self, 'catalog/upload')
