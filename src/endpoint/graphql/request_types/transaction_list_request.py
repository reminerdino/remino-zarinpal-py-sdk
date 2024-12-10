import json
from src.endpoint.fillable import Fillable
from src.validator import Validator


class TransactionListRequest(Fillable):


    def __init__(self, inputs: dict[str, str] | None = None) -> None:

        self.terminal_id: str = ''
        self.filter: str | None = None
        self.id: str | None = None
        self.reference_id: str | None = None
        self.rrn: str | None = None
        self.card_pan: str | None = None
        self.email: str | None = None
        self.mobile: str | None = None
        self.description: str | None = None
        self.limit: int | None = 25  # Default limit is 25
        self.offset: int | None = 0  # Default offset is 0
        super().__init__(inputs)

    def validate(self) -> None:

        Validator.validate_terminal_id(self.terminal_id)
        Validator.validate_filter(self.filter)
        Validator.validate_email(self.email)
        Validator.validate_mobile(self.mobile)
        Validator.validate_card_pan(self.card_pan)
        Validator.validate_limit(self.limit)
        Validator.validate_offset(self.offset)

    def to_graphql(self) -> str:

        self.validate()

        query = """
            query Sessions(
                $terminal_id: ID!,
                $filter: FilterEnum,
                $id: ID,
                $reference_id: String,
                $rrn: String,
                $card_pan: String,
                $email: String,
                $mobile: CellNumber,
                $description: String,
                $limit: Int,
                $offset: Int
            ) {
                Session(
                    terminal_id: $terminal_id,
                    filter: $filter,
                    id: $id,
                    reference_id: $reference_id,
                    rrn: $rrn,
                    card_pan: $card_pan,
                    email: $email,
                    mobile: $mobile,
                    description: $description,
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
            'terminal_id': self.terminal_id,
            'filter': self.filter,
            'id': self.id,
            'reference_id': self.reference_id,
            'rrn': self.rrn,
            'card_pan': self.card_pan,
            'email': self.email,
            'mobile': self.mobile,
            'description': self.description,
            'limit': self.limit,
            'offset': self.offset,
        }

        try:
            graphql_request = json.dumps({
                'query': query,
                'variables': variables
            }, ensure_ascii=False)
        except json.JSONDecodeError as e:
            raise ValueError(f"Error encoding to JSON: {e}")

        return graphql_request
