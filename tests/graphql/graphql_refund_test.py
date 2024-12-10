import unittest
from unittest.mock import Mock
from src.client import ClientBuilder
from src.options import Options
from src.endpoint.graphql.refund_service import RefundService
from src.endpoint.graphql.request_types import RefundRequest
from src.endpoint.graphql.response_types import RefundResponse

class GraphQLRefundTest(unittest.TestCase):
    def setUp(self):

        super().setUp()

        client_builder = ClientBuilder()
        self.options = Options(
            client_builder=client_builder,
            access_token="your_access_token"
        )

        self.refund_service = RefundService(client_builder, self.options)

    def test_refund(self):

        refund_request = RefundRequest()
        refund_request.session_id = '385404539'
        refund_request.amount = 20000
        refund_request.description = 'Test Refund'

        mock_response = RefundResponse(
            id='1234567890',
            terminal_id='238',
            amount=20000,
            timeline={
                'refund_amount': 20000,
                'refund_time': '2024-08-25T15:00:00+03:30',
                'refund_status': 'PENDING'
            }
        )

        refund_service_mock = Mock(spec=RefundService)
        refund_service_mock.refund.return_value = mock_response

        response = refund_service_mock.refund(refund_request)

        # بررسی نتایج تست
        self.assertEqual(response.id, '1234567890')
        self.assertEqual(response.amount, 20000)
        self.assertIn('refund_status', response.timeline)


if __name__ == "__main__":
    unittest.main()
