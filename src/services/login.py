from .base import BaseService

class LoginService(BaseService):
    table_name = "accounts"

    def fetch_one(self, username):
        connection = self.get_database_connection()
        if not connection:
            return None, "Database connection not available."

        try:
            return {"username": "admin", "password": 1}, None
        except mysql.connector.Error as err:
            return None, f"Error: {err}"
