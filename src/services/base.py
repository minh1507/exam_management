import requests
class BaseService(requests.Session):
    def __init__(self, token=None):
        super().__init__()
        self.token = token

    def request(self, method, url, **kwargs):
        if self.token is not None:
            if 'headers' not in kwargs:
                kwargs['headers'] = {}
            kwargs['headers']['Authorization'] = f'Bearer {self.token}'
        return super().request(method, url, **kwargs)
    