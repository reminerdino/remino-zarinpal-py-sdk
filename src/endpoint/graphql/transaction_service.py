

from src.endpoint.graphql.base_graphql_service import BaseGraphQLService
from src.validator import Validator


class TransactionService(BaseGraphQLService):
    def __init__(self, client, options):
        super().__init__(client, options)

    def list(self, data: dict) -> dict:

        Validator.validate_terminal_id(data['terminalId'])
        if 'filter' in data:
            Validator.validate_filter(data['filter'])
        if 'limit' in data:
            Validator.validate_limit(data['limit'])
        if 'offset' in data:
            Validator.validate_offset(data['offset'])

        query = """
        query GetTransactions($terminal_id: ID!, $filter: String, $limit: Int, $offset: Int) {
            transactions: GetTransactions(
                terminal_id: $terminal_id,
                filter: $filter,
                limit: $limit,
                offset: $offset
            ) {
                id,
                status,
                amount,
                description,
                created_at
            }
        }
        """

        variables = {
            "terminal_id": data["terminalId"],
            "filter": data.get("filter"),
            "limit": data.get("limit"),
            "offset": data.get("offset"),
        }

        return self.http_handler(query, variables)
