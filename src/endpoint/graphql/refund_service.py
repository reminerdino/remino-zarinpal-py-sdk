

from src.endpoint.graphql.base_graphql_service import BaseGraphQLService
from src.validator import Validator


class RefundService(BaseGraphQLService):
    def __init__(self, client, options):
        super().__init__(client, options)

    def create(self, data: dict) -> dict:
        # Validate input data
        Validator.validate_session_id(data['sessionId'])
        Validator.validate_amount(data['amount'])
        if 'method' in data:
            Validator.validate_method(data['method'])
        if 'reason' in data:
            Validator.validate_reason(data['reason'])

        query = """
        mutation AddRefund(
            $session_id: ID!,
            $amount: BigInteger!,
            $description: String,
            $method: InstantPayoutActionTypeEnum,
            $reason: RefundReasonEnum
        ) {
            resource: AddRefund(
                session_id: $session_id,
                amount: $amount,
                description: $description,
                method: $method,
                reason: $reason
            ) {
                terminal_id,
                id,
                amount,
                timeline {
                    refund_amount,
                    refund_time,
                    refund_status
                }
            }
        }
        """
        variables = {
            "session_id": data["sessionId"],
            "amount": data["amount"],
            "description": data.get("description"),
            "method": data.get("method"),
            "reason": data.get("reason"),
        }

        # Make the GraphQL request
        return self.http_handler(self.graphql_url, query, variables)

    def retrieve(self, refund_id: str) -> dict:
        query = """
        query GetRefund($id: ID!) {
            refund: GetRefund(id: $id) {
                id,
                amount,
                status,
                created_at,
                description
            }
        }
        """
        variables = {"id": refund_id}

        # Make the GraphQL request
        return self.http_handler(self.graphql_url, query, variables)

    def list(self, data: dict) -> dict:
        # Validate input data
        Validator.validate_terminal_id(data['terminalId'])
        if 'limit' in data:
            Validator.validate_limit(data['limit'])
        if 'offset' in data:
            Validator.validate_offset(data['offset'])

        query = """
        query GetRefunds($terminal_id: ID!, $limit: Int, $offset: Int) {
            refunds: GetRefunds(
                terminal_id: $terminal_id,
                limit: $limit,
                offset: $offset
            ) {
                id,
                amount,
                status,
                created_at,
                description
            }
        }
        """
        variables = {
            "terminal_id": data["terminalId"],
            "limit": data.get("limit"),
            "offset": data.get("offset"),
        }

        # Make the GraphQL request
        return self.http_handler(self.graphql_url, query, variables)
