# zarinpal_sdk/endpoint/graphql/base_graphql_service.py

import json
from typing import Any, Dict
import httpx

from src.client import ClientBuilder
from src.options import Options
from src.http_client.exceptions.response_exception import ResponseException


class BaseGraphQLService:
    def __init__(self, client_builder: ClientBuilder, options: Options):
        self.client_builder = client_builder
        self.options = options
        self.graphql_url = options.get_graphql_url()

    def http_handler(self, query: str, variables: Dict[str, Any]) -> Dict[str, Any]:
        try:
            http_client = self.client_builder.get_http_client()
            headers = {
                'User-Agent': 'ZarinPal Python SDK',
                'Authorization': f'Bearer {self.options.get_access_token()}',
                'Content-Type': 'application/json',
            }
            payload = {
                "query": query,
                "variables": variables
            }
            response = http_client.post(self.graphql_url, headers=headers, json=payload)

            self.check_http_error(response)

            response_data = response.json()

        except json.JSONDecodeError as e:
            raise ResponseException(f"JSON parsing error: {str(e)}", details={"details": str(e)})
        except ResponseException as e:
            raise ResponseException(f"Response error: {str(e)}", details=e.error_details)

        return self.check_graphql_error(response_data)

    @staticmethod
    def check_http_error(response: httpx.Response) -> None:
        if response.status_code != 200:
            try:
                parsed_body = response.json()
            except json.JSONDecodeError:
                parsed_body = {}

            error_data = {
                'data': [],
                'errors': {
                    'message': response.reason_phrase,
                    'code': response.status_code,
                    'details': parsed_body or []
                }
            }

            raise ResponseException(error_data['errors']['message'], error_data['errors']['code'], error_data)

    @staticmethod
    def check_graphql_error(response: Dict[str, Any]) -> Dict[str, Any]:
        """
        بررسی خطای GraphQL در پاسخ
        """
        if 'errors' in response or not response.get('data'):
            error_details = response.get('errors', [{'message': 'Unknown error', 'code': -1}])
            raise ResponseException(f"GraphQL query error: {json.dumps(error_details)}",
                                    error_details[0].get('code', -1))

        return response

    def get_class_name(self) -> str:
        return self.__class__.__name__
