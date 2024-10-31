import mysql.connector

def conectar():
    conn = mysql.connector.connect(
        host='localhost',   # Cambia por tu host de MySQL
        user='root',        # Cambia por tu usuario de MySQL
        password='M4tsum0t017*',        # Cambia por tu contraseña de MySQL
        database='topNails'  # Cambia por tu base de datos
    )
    return conn
