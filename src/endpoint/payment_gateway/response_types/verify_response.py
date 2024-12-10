from typing import Optional
from dataclasses import dataclass
from src.endpoint.fillable import Fillable


@dataclass
class VerifyResponse(Fillable):
    """
    پاسخ تایید شده برای درخواست پرداخت از درگاه.
    """

    authority: str
    code: int
    message: str
    ref_id: str
    card_pan: str
    card_hash: str
    fee_type: str
    fee: str

    def __init__(self, authority: str, code: int, message: str,
                 ref_id: str, card_pan: str, card_hash: str, fee_type: str, fee: str):

        super().__init__()

        self.authority = authority
        self.code = code
        self.message = message
        self.ref_id = ref_id
        self.card_pan = card_pan
        self.card_hash = card_hash
        self.fee_type = fee_type
        self.fee = fee
