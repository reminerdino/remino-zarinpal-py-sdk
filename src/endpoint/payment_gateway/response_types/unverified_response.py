from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from src.endpoint.fillable import Fillable


@dataclass
class UnverifiedResponse(Fillable):

    code: int
    message: str
    authorities: List[Dict[str, Any]] = field(default_factory=list)

    def __init__(self, data: Optional[Dict[str, Any]] = None):
        super().__init__()

        if data:
            self.code = data.get('code', 0)
            self.message = data.get('message', '')

            if 'authorities' in data and isinstance(data['authorities'], list):
                for authority_data in data['authorities']:
                    self.authorities.append({
                        'authority': authority_data.get('authority', ''),
                        'amount': authority_data.get('amount', 0),
                        'callback_url': authority_data.get('callback_url', ''),
                        'referer': authority_data.get('referer', ''),
                        'date': authority_data.get('date', ''),
                    })
