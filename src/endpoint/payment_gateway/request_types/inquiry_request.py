import json
from dataclasses import dataclass, field
from typing import Optional
from src.endpoint.fillable import Fillable
from src.validator import Validator


@dataclass
class InquiryRequest(Fillable):

    merchant_id: Optional[str] = field(default=None)
    authority: str = field(default_factory=str)

    def validate(self) -> None:

        Validator.validate_merchant_id(self.merchant_id)
        Validator.validate_authority(self.authority)

    def to_string(self) -> str:

        self.validate()

        try:
            return json.dumps(
                {
                    "merchant_id": self.merchant_id,
                    "authority": self.authority
                },
                ensure_ascii=False
            )
        except (TypeError, ValueError) as e:
            raise ValueError(f"JSON encoding error: {e}")
