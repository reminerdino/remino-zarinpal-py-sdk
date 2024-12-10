from src.endpoint.fillable import Fillable


class TransactionListResponse(Fillable):

    def __init__(self, data: dict[str, any]) -> None:

        self.id: str = data.get('id', '')
        self.status: str = data.get('status', '')
        self.amount: int = data.get('amount', 0)
        self.description: str = data.get('description', '')
        self.created_at: str = data.get('created_at', '')
        super().__init__(data)
