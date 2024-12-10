import json
from src.endpoint.fillable import Fillable
from src.validator import Validator


class RefundRequest(Fillable):
    METHOD_PAYA = 'PAYA'
    METHOD_CARD = 'CARD'

    REASON_CUSTOMER_REQUEST = 'CUSTOMER_REQUEST'
    REASON_DUPLICATE_TRANSACTION = 'DUPLICATE_TRANSACTION'
    REASON_SUSPICIOUS_TRANSACTION = 'SUSPICIOUS_TRANSACTION'
    REASON_OTHER = 'OTHER'

    def __init__(self, session_id: str, amount: int, description: str,
                 method: str = METHOD_PAYA, reason: str = REASON_CUSTOMER_REQUEST):
        self.session_id: str = session_id
        self.amount: int = amount
        self.description: str = description
        self.method: str = method
        self.reason: str = reason

    def validate(self) -> None:
        """Validates the attributes of the RefundRequest object."""
        Validator.validate_session_id(self.session_id)
        Validator.validate_amount(self.amount, 20000)
        Validator.validate_method(self.method)
        Validator.validate_reason(self.reason)

    def to_graphql(self) -> str:
        """Converts the RefundRequest object to a GraphQL mutation string."""
        self.validate()

        query = '''
            mutation AddRefund($session_id: ID!, $amount: BigInteger!, $description: String, 
                               $method: InstantPayoutActionTypeEnum, $reason: RefundReasonEnum) {
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
        '''

        variables = {
            'session_id': self.session_id,
            'amount': self.amount,
            'description': self.description,
            'method': self.method,
            'reason': self.reason,
        }

        try:
            return json.dumps({
                'query': query,
                'variables': variables
            }, ensure_ascii=False)
        except json.JSONDecodeError as e:
            raise ValueError(f"Error encoding GraphQL query to JSON: {e}")
