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
    def get_all_services():
        conn = conectar()
        cursor = conn.cursor()
        query = "SELECT idServicio, Nombre, Descripcion, Precio FROM SERVICIO"
        cursor.execute(query)
        servicios = cursor.fetchall()
        cursor.close()
        conn.close()
        
        # Convierte a diccionario para mejor acceso en la plantilla
        return [
            {'idServicio': servicio[0], 'Nombre': servicio[1], 'Descripcion': servicio[2], 'Precio': servicio[3]}
            for servicio in servicios
        ]

    @staticmethod
    def get_service_price(id_servicio):
        conn = conectar()
        cursor = conn.cursor()
        query = "SELECT Precio FROM SERVICIO WHERE idServicio = %s"
        cursor.execute(query, (id_servicio,))
        precio = cursor.fetchone()  # Cambia fetchall() por fetchone() para obtener un solo resultado
        cursor.close()
        conn.close()
        
        return precio[0] if precio else None  # Retorna el precio o None si no existe
    @staticmethod
    def add_product_to_service(servicio_id, producto_id):
        conn = conectar()
        cursor = conn.cursor()
        query = "INSERT INTO ServicioProducto (idServicio, idProducto) VALUES (%s, %s)"
        cursor.execute(query, (servicio_id, producto_id))
        conn.commit()
        cursor.close()
        conn.close()
        return True