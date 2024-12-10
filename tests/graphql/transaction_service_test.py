import unittest
from unittest.mock import Mock
from src.client import ClientBuilder
from src.options import Options
from src.endpoint.graphql.transaction_service import TransactionService
from src.endpoint.graphql.response_types.transaction_list_response import TransactionListResponse
from src.endpoint.graphql.request_types.transaction_list_request import TransactionListRequest


class TransactionServiceTest(unittest.TestCase):
    def setUp(self):

        super().setUp()

        client_builder = ClientBuilder()
        self.options = Options(
            client_builder=client_builder,
            access_token="your_access_token",
            graphql_url="https://your-graphql-endpoint"
        )

        self.transaction_service = Mock(spec=TransactionService)
        self.transaction_service.get_transactions.return_value = [
            TransactionListResponse(
                id="1234567890",
                status="PAID",
                amount=10000,
                description="Test transaction",
                created_at="2024-08-25T15:00:00+03:30"
            )
        ]

    def test_get_transactions(self):

        transaction_request = TransactionListRequest()
        transaction_request.terminal_id = '238'

        transactions = self.transaction_service.get_transactions(transaction_request)

        self.assertEqual(len(transactions), 1)
        self.assertEqual(transactions[0].id, "1234567890")
        self.assertEqual(transactions[0].status, "PAID")
        self.assertEqual(transactions[0].amount, 10000)
        self.assertEqual(transactions[0].description, "Test transaction")


if __name__ == "__main__":
    unittest.main()
