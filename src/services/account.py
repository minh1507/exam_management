from .base import BaseService

class AccountService(BaseService):
    def fetch_account(self):
        response = self.get(self.wrap_url("user/"))
        return response.json()["data"]
    
    def create_account(self, new_data):
        response = self.post(self.wrap_url("user/"), json={
            "username": new_data[0],
            "password": new_data[1],
            "role": new_data[2]
        })
        return response.json()
    def delete_account(self, account_id):
        response = self.delete(self.wrap_url(f"user/{account_id}"))
        return  response.json()