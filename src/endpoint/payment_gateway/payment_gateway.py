import json
from typing import Any, Dict

#from src.endpoint.payment_gateway.response_types import (
   # request_response,
   # unverified_response,
  #  verify_response
#)
from src.endpoint.payment_gateway.response_types.verify_response import (
    VerifyResponse
)
from src.endpoint.payment_gateway.response_types.request_response import (
    RequestResponse
)
from src.endpoint.payment_gateway.response_types.unverified_response import (
    UnverifiedResponse
)
from src.http_client.exceptions.payment_gateway_exception import PaymentGatewayException
from src.http_client.exceptions.response_exception import ResponseException
from src.zarinpal import ZarinPal


class PaymentGateway:

    BASE_URL = '/pg/v4/payment/'
    START_PAY = '/pg/StartPay/'
    REQUEST_URI = BASE_URL + 'request.json'
    VERIFY_URI = BASE_URL + 'verify.json'
    UNVERIFIED_URI = BASE_URL + 'unVerified.json'
    REVERSE_URI = BASE_URL + 'reverse.json'
    INQUIRY_URI = BASE_URL + 'inquiry.json'

    def __init__(self, sdk: ZarinPal) -> None:

        self.sdk = sdk

    def request(self, request: Any) -> RequestResponse:
        self.fill_merchant_id(request)
        response = self.http_handler(self.REQUEST_URI, request.to_string())
        return RequestResponse(response['data'])

    def get_redirect_url(self, authority: str) -> str:
        base_url = str(self.sdk.get_options().get_base_url())
        return f"{base_url.rstrip('/')}{self.START_PAY}{authority}"

    def verify(self, request: Any) -> VerifyResponse:
        self.fill_merchant_id(request)
        response = self.http_handler(self.VERIFY_URI, request.to_string())
        return VerifyResponse(response['data'])

    def unverified(self, request: Any) -> UnverifiedResponse:
        self.fill_merchant_id(request)
        response = self.http_handler(self.UNVERIFIED_URI, request.to_string())
        return UnverifiedResponse(response['data'])

    def reverse(self, request: Any) -> RequestResponse:
        self.fill_merchant_id(request)
        response = self.http_handler(self.REVERSE_URI, request.to_string())
        return RequestResponse(response['data'])

    def inquiry(self, request: Any) -> RequestResponse:
        self.fill_merchant_id(request)
        response = self.http_handler(self.INQUIRY_URI, request.to_string())
        return RequestResponse(response['data'])

    def fill_merchant_id(self, request: Any) -> None:
        """
        Ensures that the merchant ID is present in the request.
        """
        if getattr(request, 'merchant_id', None) is None:
            request.merchant_id = self.sdk.get_merchant_id()

    def http_handler(self, uri: str, body: str) -> Dict[str, Any]:
        """
        Handles HTTP requests to the ZarinPal API.

        :param uri: The endpoint URI.
        :param body: The body of the request.
        :return: The parsed JSON response from the API.
        """
        try:
            full_uri = f"{self.sdk.get_options().get_base_url()}{uri}"
            response = self.sdk.get_http_client().post(full_uri, {}, body)
            self.check_http_error(response)
            response_data = json.loads(response.text)
        except json.JSONDecodeError as e:
            raise ResponseException(
                f"JSON parsing error: {e.msg}",
                -98,
                None,
                {'details': e.msg}
            ) from e
        except ResponseException as e:
            raise ResponseException(
                f"Response error: {e}",
                e.code,
                None,
                e.get_error_details()
            ) from e

        return self.check_payment_gateway_error(response_data)

    def check_http_error(self, response: Any) -> None:
        """
        Checks for HTTP errors in the response.

        :param response: The response object.
        """
        status_code = response.status_code
        if status_code != 200:
            body = response.text
            parsed_body = json.loads(body) if body else {}

            if 'errors' in parsed_body:
                error_data = parsed_body
            else:
                error_data = {
                    'data': [],
                    'errors': {
                        'message': response.reason,
                        'code': status_code,
                        'validations': []
                    }
                }

            raise ResponseException(
                error_data['errors']['message'],
                error_data['errors']['code'],
                None,
                error_data
            )

    def check_payment_gateway_error(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Checks for errors returned by the payment gateway.

        :param response: The response data.
        :return: The response data if no errors are present.
        """
        if 'errors' in response or 'data' not in response:
            error_details = response.get('errors', {'message': 'Unknown error', 'code': -1})
            raise PaymentGatewayException(
                error_details['message'],
                error_details['code'],
                None,
                response
            )

        return response
