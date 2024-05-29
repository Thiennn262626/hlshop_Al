import os
from dotenv import load_dotenv
import pyodbc

load_dotenv()

class ConnectionHandler:
    def __init__(self):
        connection_string = os.getenv("SQL_SERVER_STRING")
        print("connection_string: ", connection_string)
        self.conn = pyodbc.connect(connection_string)
        print("ConnectionHandler init.", self.conn)

    def fetch_data(self, query):
        cursor = self.conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        return rows

db_connection = ConnectionHandler()
