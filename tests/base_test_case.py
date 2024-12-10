import unittest
from unittest.mock import Mock
from src.options import Options


class BaseTestCase(unittest.TestCase):
    def setUp(self):

        self.mock_client = Mock()
        self.options = Options(
            access_token="mock-access-token",
            merchant_id="67887a6d-e2f8-4de2-86b1-8db27bc171b5"
        )

    def get_mock_client(self):

        return self.mock_client

    def get_options(self):

        return self.options


if __name__ == "__main__":
    unittest.main()
