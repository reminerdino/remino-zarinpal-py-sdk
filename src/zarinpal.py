import requests
from typing import Optional


class Options:
    def __init__(self, base_url: str = "https://api.zarinpal.com", merchant_id: Optional[str] = None):
        self.base_url = base_url
        self.merchant_id = merchant_id
        self.headers = {
            "User-Agent": f"ZarinPalSdk/v.1.0 (python {self.get_python_version()})",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def get_base_url(self) -> str:
        return self.base_url

    def get_merchant_id(self) -> Optional[str]:
        return self.merchant_id

    def get_python_version(self) -> str:
        import sys
        return sys.version


class ZarinPal:
    USER_AGENT = f"ZarinPalSdk/v.1.0 (python)"

    def __init__(self, options: Optional[Options] = None):
        self.options = options or Options()
        self.http_client = requests.Session()
        self.http_client.headers.update(self.options.headers)

    def get_class_name(self) -> str:
        return self.__class__.__name__

    def get_options(self) -> Options:
        return self.options

    def payment_gateway(self) -> 'PaymentGateway':
        return PaymentGateway(self)

    def transaction_service(self) -> 'TransactionService':
        return TransactionService(self.http_client, self.options)

    def refund_service(self) -> 'RefundService':
        return RefundService(self.http_client, self.options)

    def get_merchant_id(self) -> Optional[str]:
        return self.options.get_merchant_id()

    def get_http_client(self) -> requests.Session:
        return self.http_client

    def set_http_client(self, client: requests.Session) -> None:
        self.http_client = client


class PaymentGateway:
    def __init__(self, sdk: ZarinPal):
        self.sdk = sdk




class TransactionService:
    def __init__(self, http_client: requests.Session, options: Options):
        self.http_client = http_client
        self.options = options




class RefundService:
    def __init__(self, http_client: requests.Session, options: Options):
        self.http_client = http_client
        self.options = options


