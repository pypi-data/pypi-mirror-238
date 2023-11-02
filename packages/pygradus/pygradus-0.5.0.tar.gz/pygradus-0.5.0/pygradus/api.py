import requests
from copy import deepcopy
from pygradus.config import settings as st


HEADERS = {
    "accept": "application/json",
}

API_MODE = {"post": requests.post, "get": requests.get}


def send_request(
    mode: str,
    url: str,
    data: dict = None,
    json: dict = None,
    token: str = "",
):

    header = deepcopy(HEADERS)
    header["Content-Type"] = st[mode]["content-type"]
    if token:
        header["Authorization"] = token

    if url is None:
        url = st.BASE_URL
    url += st[mode]["url"]

    func = API_MODE[st[mode]["mode"]]

    response = func(url, json=json, data=data, headers=header)
    return response
