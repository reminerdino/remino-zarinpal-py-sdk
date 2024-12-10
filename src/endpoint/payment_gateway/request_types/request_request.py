import json
from dataclasses import dataclass, field
from typing import Optional, List
from src.endpoint.fillable import Fillable
from src.validator import Validator


@dataclass
class RequestRequest(Fillable):

    amount: int
    description: str
    callback_url: str

    merchant_id: Optional[str] = field(default=None)
    mobile: Optional[str] = field(default=None)
    email: Optional[str] = field(default=None)
    referrer_id: Optional[str] = field(default=None)
    currency: Optional[str] = field(default=None)
    wages: Optional[List[str]] = field(default=None)
    card_pan: Optional[str] = field(default=None)

    def validate(self) -> None:

        Validator.validate_merchant_id(self.merchant_id)
        Validator.validate_amount(self.amount)
        Validator.validate_callback_url(self.callback_url)
        Validator.validate_mobile(self.mobile)
        Validator.validate_email(self.email)
        Validator.validate_currency(self.currency)
        Validator.validate_wages(self.wages)
        Validator.validate_card_pan(self.card_pan)

    def to_string(self) -> str:

        self.validate()

        data = {
            "merchant_id": self.merchant_id,
            "amount": self.amount,
            "callback_url": self.callback_url,
            "description": self.description,
            "metadata": {
                "mobile": self.mobile,
                "email": self.email,
                "referrer_id": self.referrer_id,
            }
        }

        if self.currency:
            data['currency'] = self.currency

        if self.wages:
            data['wages'] = self.wages

        if self.card_pan:
            data['metadata']['card_pan'] = self.card_pan

        try:
            return json.dumps(data, ensure_ascii=False)
        except (TypeError, ValueError) as e:
            raise ValueError(f"JSON encoding error: {e}")
