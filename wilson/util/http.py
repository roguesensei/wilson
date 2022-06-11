import requests


class Http:
    def __init__(self, base_url: str):
        self._base_url = base_url
        self._session = requests.Session()

    def get(self, url: str) -> requests.Response:
        return self._session.get(f'{self._base_url}{url}')
