import json
from dataclasses import dataclass, field
from typing import Optional
from src.endpoint.fillable import Fillable
from src.validator import Validator


@dataclass
class VerifyRequest(Fillable):

    amount: int
    authority: str
    merchant_id: Optional[str] = field(default=None)

    def validate(self) -> None:

        Validator.validate_merchant_id(self.merchant_id)
        Validator.validate_amount(self.amount)
        Validator.validate_authority(self.authority)

    def to_string(self) -> str:

        self.validate()

        data = {
            "merchant_id": self.merchant_id,
            "amount": self.amount,
            "authority": self.authority
        }

        try:
            return json.dumps(data, ensure_ascii=False)
        except json.JSONDecodeError as e:
            raise ValueError(f"JSON encoding error: {e}")
