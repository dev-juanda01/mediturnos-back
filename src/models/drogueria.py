import mysql.connector
#from mysql.connector import Error
from config import Config



def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DB
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

class Drogueria:
    def __init__(self, id_drogueria=None, nombre=None, direccion=None, codigo=None):
        self.id_drogueria = id_drogueria
        self.nombre = nombre
        self.direccion = direccion
        self.codigo = codigo

    @staticmethod
    def get_all():
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM drogueria")
            droguerias = cursor.fetchall()
            cursor.close()
            connection.close()
            return droguerias
        return []

    @staticmethod
    def create(nombre, direccion, codigo):
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO drogueria (nombre, direccion, codigo) VALUES (%s, %s, %s)", (nombre, direccion, codigo))
            connection.commit()
            cursor.close()
            connection.close()
            return True
        return False
