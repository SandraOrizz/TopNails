from app.db import conectar

class Servicio:
    @staticmethod
    def create_servicio(nombre, descripcion, precio):
        conn = conectar()
        cursor = conn.cursor()
        query = "INSERT INTO SERVICIO (Nombre, Descripcion, Precio) VALUES (%s, %s, %s)"
        cursor.execute(query, (nombre, descripcion, precio))
        conn.commit()
        cursor.close()
        conn.close()
        return cursor.lastrowid  # Devuelve el ID del servicio creado

    @staticmethod
    def get_servicios():
        conn = conectar()
        cursor = conn.cursor()
        query = "SELECT * FROM SERVICIO"
        cursor.execute(query)
        servicios = cursor.fetchall()
        cursor.close()
        conn.close()
        return servicios
