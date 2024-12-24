import unittest
import json
from unittest.mock import Mock
from src.options import Options
from src.zarinpal import ZarinPal
from src.endpoint.payment_gateway.payment_gateway import PaymentGateway
from src.endpoint.payment_gateway.request_types.reverse_request import ReverseRequest
from src.endpoint.payment_gateway.request_types.inquiry_request import InquiryRequest
from src.endpoint.payment_gateway.request_types.request_request import RequestRequest
from src.endpoint.payment_gateway.request_types.unverified_request import UnverifiedRequest
from src.endpoint.payment_gateway.request_types.verify_request import VerifyRequest


class PaymentGatewayTest(unittest.TestCase, Options):
    def setUp(self):

        super().setUp()

        self.client_mock = Mock()

        zarinpal = ZarinPal(Options)
        zarinpal.set_http_client(self.client_mock)

        self.gateway = PaymentGateway(zarinpal)

    def create_mock_response(self, body, status_code=200):

        stream = Mock()
        stream.get_contents.return_value = json.dumps(body)

        response = Mock()
        response.get_body.return_value = stream
        response.get_status_code.return_value = status_code

        return response

    def test_request(self):

        response_body = {
            'data': {
                'authority': 'A0000000000000000000000000012b4A6',
            },
            'errors': []
        }

        self.client_mock.post.return_value = self.create_mock_response(response_body)

        request = RequestRequest()
        request.amount = 10000
        request.description = 'Test Payment'
        request.callback_url = 'https://callback.url'
        request.mobile = '09370000000'
        request.email = 'test@example.com'

        response = self.gateway.request(request)
        self.assertEqual('A0000000000000000000000000012b4A6', response.authority)

    def test_verify(self):

        response_body = {
            'data': {
                'code': 100,
                'ref_id': '1234567890',
            },
            'errors': []
        }

        self.client_mock.post.return_value = self.create_mock_response(response_body)

        verify = VerifyRequest()
        verify.amount = 15000
        verify.authority = 'A000000000000000000000000000ydq5y838'

        response = self.gateway.verify(verify)
        self.assertEqual(100, response.code)

    def test_unverified(self):

        response_body = {
            'data': {
                'code': 100,
                'message': 'Success',
                'authorities': [
                    {
                        'authority': 'A000000000000000000000000000ydq5y838',
                        'amount': 50000,
                        'callback_url': 'https://example.com/callback',
                        'referer': 'https://example.com/referer',
                        'date': '2024-09-22 10:00:00'
                    },
                    {
                        'authority': 'A000000000000000000000000000ydq5y839',
                        'amount': 75000,
                        'callback_url': 'https://example.com/callback2',
                        'referer': 'https://example.com/referer2',
                        'date': '2024-09-22 12:00:00'
                    }
                ],
            },
            'errors': []
        }

        self.client_mock.post.return_value = self.create_mock_response(response_body)

        unverified = UnverifiedRequest()

        response = self.gateway.unverified(unverified)

        self.assertEqual(100, response.code)
        self.assertEqual(len(response.authorities), 2)
        self.assertEqual('A000000000000000000000000000ydq5y838', response.authorities[0]['authority'])
        self.assertEqual(50000, response.authorities[0]['amount'])
        self.assertEqual('https://example.com/callback', response.authorities[0]['callback_url'])
        self.assertEqual('2024-09-22 10:00:00', response.authorities[0]['date'])
        self.assertEqual('A000000000000000000000000000ydq5y839', response.authorities[1]['authority'])
        self.assertEqual(75000, response.authorities[1]['amount'])
        self.assertEqual('https://example.com/callback2', response.authorities[1]['callback_url'])
        self.assertEqual('2024-09-22 12:00:00', response.authorities[1]['date'])

    def test_reverse(self):

        response_body = {
            'data': {
                'status': 'Success',
            },
            'errors': []
        }

        self.client_mock.post.return_value = self.create_mock_response(response_body)

        reverse_request = ReverseRequest()
        reverse_request.authority = 'A000000000000000000000000000ydq5y838'

        response = self.gateway.reverse(reverse_request)
        self.assertEqual('Success', response.status)

    def test_inquiry(self):
        response_body = {
            'data': {
                'amount': 15000,
            },
            'errors': []
        }
        self.client_mock.post.return_value = self.create_mock_response(response_body)

        inquiry_request = InquiryRequest()
        inquiry_request.authority = 'A000000000000000000000000000ydq5y838'

        response = self.gateway.inquiry(inquiry_request)
        self.assertEqual(15000, response.amount)


if __name__ == '__main__':
    unittest.main()
