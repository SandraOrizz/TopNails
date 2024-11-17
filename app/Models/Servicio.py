from app.db import conectar
import base64
class Servicio:
    @staticmethod
    def create_servicio(nombre, descripcion, precio, imagen):
        conn = conectar()
        cursor = conn.cursor()
        
        # Leer la imagen en binario
        imagen_binario = None
        if imagen:
            imagen_binario = imagen.read()  # Leer el archivo de imagen cargado
        
        # Insertar el servicio junto con la imagen
        query = """
            INSERT INTO SERVICIO (Nombre, Descripcion, Precio, Imagen)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (nombre, descripcion, precio, imagen_binario))
        conn.commit()
        cursor.close()
        conn.close()
        return cursor.lastrowid  # Devuelve el ID del servicio creado

    @staticmethod
    def get_all_services():
        conn = conectar()
        cursor = conn.cursor()
        query = "SELECT idServicio, Nombre, Descripcion, Precio, Imagen FROM SERVICIO"
        cursor.execute(query)
        servicios = cursor.fetchall()
        cursor.close()
        conn.close()
        
        # Convierte la imagen a base64 y devuelve los servicios con sus imágenes
        return [
            {
                'idServicio': servicio[0],
                'Nombre': servicio[1],
                'Descripcion': servicio[2],
                'Precio': servicio[3],
                'Imagen': base64.b64encode(servicio[4]).decode('utf-8') if servicio[4] else None  # Convertir la imagen binaria a base64
            }
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