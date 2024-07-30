import requests
import os
from dotenv import load_dotenv

load_dotenv()

class BaseService(requests.Session):
    url = os.getenv("BASE_API_URL")

    def __init__(self, token=None):
        super().__init__()
        self.token = token

    def request(self, method, url, **kwargs):
        if self.token is not None:
            if 'headers' not in kwargs:
                kwargs['headers'] = {}
            kwargs['headers']['Authorization'] = f'Bearer {self.token}'
        return super().request(method, url, **kwargs)
    
    def wrap_url(self, path):
        return self.url + path
    