from app.db import conectar

class Producto:
    @staticmethod
    def create_producto(nombre, descripcion, precio):
        conn = conectar()
        cursor = conn.cursor()
        query = "INSERT INTO PRODUCTO (Nombre, Descripcion, Precio) VALUES (%s, %s, %s)"
        cursor.execute(query, (nombre, descripcion, precio))
        conn.commit()
        cursor.close()
        conn.close()
        return cursor.lastrowid  # Devuelve el ID del producto creado

    @staticmethod
    def get_productos():
        conn = conectar()
        cursor = conn.cursor()
        query = "SELECT * FROM PRODUCTO"
        cursor.execute(query)
        productos = cursor.fetchall()
        cursor.close()
        conn.close()
        return productos
