from dotenv import load_dotenv
import os
import mysql.connector
load_dotenv()

class BaseService:
    table_name = ''
    def __init__(self):
        self.db_config = {
            'host': os.getenv("DB_HOST"),
            'user': os.getenv("DB_USER"),
            'port': os.getenv("DB_PORT"),
            'password': os.getenv("DB_PASSWORD"),
            'database': os.getenv("DB_NAME"),
            'collation': os.getenv("DB_COLLATION"),
        }

    def get_database_connection(self):
        try:
            connection = mysql.connector.connect(**self.db_config)
            return connection
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None