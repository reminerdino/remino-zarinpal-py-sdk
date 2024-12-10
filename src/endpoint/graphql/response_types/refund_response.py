from src.endpoint.fillable import Fillable


class RefundResponse(Fillable):

    def __init__(self, data: dict[str, any]) -> None:

        self.terminal_id: str = data.get('terminal_id', '')
        self.id: str = data.get('id', '')
        self.amount: int = data.get('amount', 0)
        self.timeline: list[dict] = data.get('timeline', [])
        super().__init__(data)
