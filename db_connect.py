import mysql.connector

class Database:
    def __init__(self) -> None:
        self.config = {
            'user': 'root',
            'password': '',
            'host': 'localhost',
            'database': 'syntec_db',
        }

    def query(self, query):
        # Abrir uma nova conexão a cada query
        connection = mysql.connector.connect(**self.config)
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        connection.close()  # Fechar a conexão após a consulta
        return results

db = Database()
