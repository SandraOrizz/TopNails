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
    def get_all_products():
        conn = conectar()
        cursor = conn.cursor()
        query = "SELECT idProducto, Nombre, Descripcion, Precio FROM PRODUCTO"
        cursor.execute(query)
        productos = cursor.fetchall()
        cursor.close()
        conn.close()
        
        # Convierte a diccionario para mejor acceso en la plantilla
        return [
            {'idProducto': producto[0], 'Nombre': producto[1], 'Descripcion': producto[2], 'Precio': producto[3]}
            for producto in productos
        ]

    @staticmethod
    def get_product_price(id_producto):
        conn = conectar()
        cursor = conn.cursor()
        query = "SELECT Precio FROM PRODUCTO WHERE idProducto = %s"
        cursor.execute(query, (id_producto,))
        precio = cursor.fetchone()  # Cambia fetchall() por fetchone() para obtener un solo resultado
        cursor.close()
        conn.close()
        
        return precio[0] if precio else None  # Retorna el precio o None si no existe
