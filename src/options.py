

import os
from typing import Optional, Any, Dict
from urllib.parse import urlparse


class ClientBuilder:

    pass


class UriFactory:
    @staticmethod
    def create_uri(url: str):
        return urlparse(url)


class Options:
    def __init__(self, options: Optional[Dict[str, Any]] = None):
        if options is None:
            options = {}

        env_vars = dict(os.environ)

        self.options = {
            'client_builder': options.get('client_builder', ClientBuilder()),
            'uri_factory': options.get('uri_factory', UriFactory()),
            'base_url': self.array_get(env_vars, 'ZARINPAL_BASE_URL', 'https://payment.zarinpal.com'),
            'sandbox_base_url': self.array_get(env_vars, 'ZARINPAL_SANDBOX_BASE_URL', 'https://sandbox.zarinpal.com'),
            'merchant_id': self.array_get(env_vars, 'ZARINPAL_MERCHANT_KEY', 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'),
            'graphql_url': self.array_get(env_vars, 'ZARINPAL_GRAPHQL_URL',
                                          'https://next.zarinpal.com/api/v4/graphql/'),
            'access_token': self.array_get(env_vars, 'ZARINPAL_ACCESS_TOKEN', ''),
            'sandbox': self.array_get(env_vars, 'ZARINPAL_SANDBOX', 'false').lower() == 'true',
        }

        self.validate_options()

    @staticmethod
    def array_get(array: dict, key: str, default: Optional[str] = None) -> Optional[str]:
        return array.get(key, default) if array.get(key, '') != '' else default

    def validate_options(self):
        if not isinstance(self.options['client_builder'], ClientBuilder):
            raise TypeError("client_builder must be of type ClientBuilder")
        if not isinstance(self.options['uri_factory'], UriFactory):
            raise TypeError("uri_factory must be of type UriFactory")
        if not isinstance(self.options['base_url'], str):
            raise TypeError("base_url must be a string")
        if not isinstance(self.options['sandbox_base_url'], str):
            raise TypeError("sandbox_base_url must be a string")
        if not isinstance(self.options['merchant_id'], str):
            raise TypeError("merchant_id must be a string")
        if not isinstance(self.options['graphql_url'], str):
            raise TypeError("graphql_url must be a string")
        if not isinstance(self.options['access_token'], str):
            raise TypeError("access_token must be a string")
        if not isinstance(self.options['sandbox'], bool):
            raise TypeError("sandbox must be a boolean")

    def get_client_builder(self) -> ClientBuilder:
        return self.options['client_builder']

    def get_base_url(self) -> str:
        url = self.options['sandbox_base_url'] if self.options['sandbox'] else self.options['base_url']
        return self.get_uri_factory().create_uri(url).geturl()

    def get_uri_factory(self) -> UriFactory:
        return self.options['uri_factory']

    def get_merchant_id(self) -> str:
        return self.options['merchant_id']

    def get_graphql_url(self) -> str:
        return self.options['graphql_url']

    def get_access_token(self) -> str:
        return self.options['access_token']
