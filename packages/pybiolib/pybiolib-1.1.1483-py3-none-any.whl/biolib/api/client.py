import json
import time
import socket
import urllib.request
import urllib.parse
from http.client import HTTPResponse
from urllib.parse import urljoin

from requests import HTTPError

from biolib.biolib_logging import logger_no_user_data
from biolib.typing_utils import Dict, Optional, Union
from biolib.biolib_api_client import BiolibApiClient as DeprecatedApiClient

OptionalHeaders = Optional[Dict[str, Union[str, None]]]


class BioLibHTTPResponse:
    def __init__(self, response: HTTPResponse):
        self.status_code = response.status
        self.content = response.read()
        self.url = response.geturl()

    @property
    def text(self):
        return self.content.decode()

    @property
    def ok(self):  # pylint: disable=invalid-name
        return self.status_code < 400

    def json(self):
        return json.loads(self.content.decode())

    def raise_for_status(self):
        # Logic taken from `requests.Response.raise_for_status()`
        http_error_msg = ''
        if 400 <= self.status_code < 500:
            http_error_msg = u'%s Client Error: %s for url: %s' % (self.status_code, self.text, self.url)

        elif 500 <= self.status_code < 600:
            http_error_msg = u'%s Server Error: %s for url: %s' % (self.status_code, self.text, self.url)

        if http_error_msg:
            raise HTTPError(http_error_msg, response=self)


class ApiClient:
    def get(
            self,
            path: str,
            params: Optional[Dict[str, Union[str, int]]] = None,
            headers: OptionalHeaders = None,
            authenticate: bool = True,
    ) -> BioLibHTTPResponse:
        url = self._get_absolute_url(path, query_params=params)
        req = urllib.request.Request(url, headers=self._get_headers(headers, authenticate))
        retries = 10
        for retry_count in range(retries):
            if retry_count > 0:
                time.sleep(5 * retry_count)
                logger_no_user_data.debug('Retrying HTTP GET request...')
            try:
                with urllib.request.urlopen(req, timeout=60) as response:
                    biolib_http_response = BioLibHTTPResponse(response)
                    if biolib_http_response.status_code == 502:
                        logger_no_user_data.debug(f'HTTP GET request failed with status 502 for "{url}"')
                        continue

                    biolib_http_response.raise_for_status()
                    return biolib_http_response

            except urllib.error.URLError as error:
                if isinstance(error.reason, socket.timeout):
                    logger_no_user_data.debug(f'HTTP GET request failed with read timeout for "{path}"')
                continue

        raise Exception(f'HTTP GET request failed after {retries} retries for "{url}"')

    def post(
            self,
            path: str,
            data: Optional[Union[Dict, bytes]] = None,
            headers: OptionalHeaders = None,
    ) -> BioLibHTTPResponse:
        retries = 3
        for retry_count in range(retries):
            if retry_count > 0:
                time.sleep(5 * retry_count)
                logger_no_user_data.debug('Retrying HTTP POST request...')
            try:
                url = self._get_absolute_url(path)
                req = urllib.request.Request(
                    url,
                    data=json.dumps(data).encode() if isinstance(data, dict) else data,
                    headers=self._get_headers(headers),
                    method='POST'
                )
                # TODO: Calculate timeout based on data size
                with urllib.request.urlopen(req, timeout=10 if isinstance(data, dict) else 180) as response:
                    biolib_http_response = BioLibHTTPResponse(response)
                    if biolib_http_response.status_code == 502:
                        logger_no_user_data.debug(f'HTTP POST request failed with status 502 for "{path}"')
                        continue

                    biolib_http_response.raise_for_status()
                    return biolib_http_response

            except urllib.error.URLError as error:
                if isinstance(error.reason, socket.timeout):
                    logger_no_user_data.debug(f'HTTP POST request failed with read timeout for "{path}"')
                continue

        raise Exception(f'HTTP POST request failed after {retries} retries for "{path}"')

    def patch(self, path: str, data: Dict, headers: OptionalHeaders = None) -> BioLibHTTPResponse:
        class PatchRequest(urllib.request.Request):
            method = "PATCH"

        url = self._get_absolute_url(path)
        req = PatchRequest(url, data=json.dumps(data).encode(), headers=self._get_headers(headers))
        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                biolib_http_response = BioLibHTTPResponse(response)
                biolib_http_response.raise_for_status()
                return biolib_http_response
        except urllib.error.URLError as error:
            raise Exception(f"Error: {error}") from error

    @staticmethod
    def _get_headers(opt_headers: OptionalHeaders = None, authenticate: bool = True) -> Dict[str, str]:
        # Only keep header keys with a value
        headers: Dict[str, str] = {key: value for key, value in (opt_headers or {}).items() if value}

        deprecated_api_client = DeprecatedApiClient.get()

        if deprecated_api_client.is_signed_in:
            deprecated_api_client.refresh_access_token()

        # Adding access_token outside is_signed_in check as job_worker.py currently sets access_token
        # without setting refresh_token
        access_token = deprecated_api_client.access_token
        if access_token and authenticate:
            headers['Authorization'] = f'Bearer {access_token}'

        return headers

    @staticmethod
    def _get_absolute_url(path: str, query_params: Optional[Dict[str, Union[str, int]]] = None) -> str:
        deprecated_api_client = DeprecatedApiClient.get()
        base_api_url = urljoin(deprecated_api_client.base_url, '/api/')
        url = urljoin(base_api_url, path.strip('/') + '/')
        if query_params:
            url = url + "?" + urllib.parse.urlencode(query_params)
        return url
