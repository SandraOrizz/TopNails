import mysql.connector

def conectar():
    conn = mysql.connector.connect(
        host='localhost',   # Cambia por tu host de MySQL
        user='root',        # Cambia por tu usuario de MySQL
        password='',        # Cambia por tu contraseña de MySQL
        database='topnails'  # Cambia por tu base de datos
    )
    return conn
