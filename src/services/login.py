from .base import BaseService
import json

class LoginService(BaseService):
    def login(self, username, password):
        response = self.post(self.wrap_url('auth/login/'), json={
            "username": username,
            "password": password
        })
        return response.json()
