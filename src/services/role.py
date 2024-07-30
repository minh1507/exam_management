from .base import BaseService

class RoleService(BaseService):
    def fetch_roles(self):
        response = self.get(self.wrap_url("role/"))
        return response.json()["data"]
