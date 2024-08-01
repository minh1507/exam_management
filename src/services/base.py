import requests
import os
from dotenv import load_dotenv
from ..common.static.global_c import Global
load_dotenv()

class BaseService(requests.Session):
    url = os.getenv("BASE_API_URL")

    def __init__(self):
        super().__init__()
        print(Global.token)
        self.token = Global.token

    def request(self, method, url, **kwargs):
        if self.token is not None:
            if 'headers' not in kwargs:
                kwargs['headers'] = {}
            kwargs['headers']['Authorization'] = f'{self.token}'
        return super().request(method, url, **kwargs)
    
    def wrap_url(self, path):
        return self.url + path
    