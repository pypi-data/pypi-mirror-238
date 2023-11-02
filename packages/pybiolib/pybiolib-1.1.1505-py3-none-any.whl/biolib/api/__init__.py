from .client import ApiClient as _ApiClient
from .http_client import HttpClient

_client = _ApiClient()
client = _client
