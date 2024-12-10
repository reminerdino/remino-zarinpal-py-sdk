from typing import Optional, List
import httpx


class Plugin:
    @staticmethod
    def process_request(request: httpx.Request) -> httpx.Request:
        # هر پلاگین می‌تواند درخواست‌ها را پردازش کند
        return request


class ClientBuilder:
    def __init__(
        self,
        timeout: int = 30,
        http_client: Optional[httpx.Client] = None,
    ):
        self.timeout = timeout
        self.plugins: List[Plugin] = []
        self.http_client = http_client or httpx.Client(timeout=self.timeout)

    def add_plugin(self, plugin: Plugin) -> None:
        self.plugins.append(plugin)

    def send_request(self, method: str, url: str, **kwargs) -> httpx.Response:
        request = httpx.Request(method, url, **kwargs)

        # پردازش درخواست با استفاده از پلاگین‌ها
        for plugin in self.plugins:
            request = plugin.process_request(request)

        # ارسال درخواست پس از پردازش توسط پلاگین‌ها
        response = self.http_client.send(request)
        return response

    def get_http_client(self) -> httpx.Client:
        return self.http_client
