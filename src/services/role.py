from .base import BaseService

class RoleService(BaseService):
    def fetch_roles(self):
        response = self.get("http://localhost:3000/api/role/")
        return response.json()["data"]
