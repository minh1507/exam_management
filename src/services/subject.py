import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()
class SubjectService:
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

    def fetch_subjects(self):
        connection = self.get_database_connection()
        if not connection:
            return None, "Database connection not available."
        
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT `order`, `code`, `name` FROM subjects order by `order` ASC")
            data = cursor.fetchall()
            cursor.close()
            connection.close()
            return data, None
        except mysql.connector.Error as err:
            return None, f"Error: {err}"

    def create_subject(self, new_data):
        connection = self.get_database_connection()
        if not connection:
            return "Database connection not available."
        
        try:
            cursor = connection.cursor()
            query = "INSERT INTO subjects (`order`, `code`, `name`) VALUES (%s, %s, %s)"
            cursor.execute(query, new_data)
            connection.commit()
            cursor.close()
            connection.close()
            return None
        except mysql.connector.Error as err:
            return f"Error: {err}"

    def update_subject(self, row_order, new_data):
        connection = self.get_database_connection()
        if not connection:
            return "Database connection not available."
        
        try:
            cursor = connection.cursor()
            query = "UPDATE subjects SET `order` = %s, `code` = %s, `name` = %s WHERE `order` = %s"
            cursor.execute(query, (*new_data, row_order))
            connection.commit()
            cursor.close()
            connection.close()
            return None
        except mysql.connector.Error as err:
            return f"Error: {err}"

    def delete_subject(self, row_order):
        connection = self.get_database_connection()
        if not connection:
            return "Database connection not available."
        
        try:
            cursor = connection.cursor()
            query = "DELETE FROM subjects WHERE `order` = %s"
            cursor.execute(query, (row_order,))
            connection.commit()
            cursor.close()
            connection.close()
            return None
        except mysql.connector.Error as err:
            return f"Error: {err}"
