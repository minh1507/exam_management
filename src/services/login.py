from .base import BaseService
import json

class LoginService(BaseService):
    def login(self, username, password):
        response = self.post("http://localhost:3000/api/auth/login/", json={
            "username": username,
            "password": password
        })
        return response.json()
