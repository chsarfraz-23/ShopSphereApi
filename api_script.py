from typing import Optional
from urllib.parse import urlencode

import requests

methods = ["POST", "GET", "UPDATE", "DELETE", "PATCH"]


def request(
        method: str, url: str,
        access_token: Optional[str] = "",
        data: Optional[dict] = {},
        headers: Optional[dict] = {},
        params: Optional[dict] = {}
):
    session = requests.Session()
    if access_token:
        headers["Authorization"] = access_token

    if params:
        params = sorted(params.items())
        url = f"{url}?{urlencode(params)}"

    request_args = {
        "method": method,
        "url": url,
        "headers": headers,
        "data": data
    }
    response = session.request(**request_args)
    processed_response = {
        "response_status": response.status_code,
        "response_body": response.text,
        "response_headers": response.headers
    }
    print("response:", processed_response)
    return processed_response


data = {'email': 'sarfraz1', 'password': '123', 'username': 'sarfraz'}
url = "http://localhost:8000/api/signup/"

request(method=methods[0], data=data, url=url)


