from dataclasses import dataclass
from src.endpoint.fillable import Fillable

@dataclass
class RequestResponse(Fillable):

    authority: str
    code: int
    message: str
    fee_type: str
    fee: int
    amount: int
    status: str
