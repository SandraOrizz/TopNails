from app.db import conectar
import base64
class Producto:
    @staticmethod
    def create_producto(nombre, descripcion, precio, imagen):
        conn = conectar()
        cursor = conn.cursor()

        try:
            imagen_binario = None
            if imagen:
                imagen_binario = imagen.read()  # Leer el archivo de imagen cargado

            query = """
                INSERT INTO PRODUCTO (Nombre, Descripcion, Precio, Imagen)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (nombre, descripcion, precio, imagen_binario))
            conn.commit()
            return cursor.lastrowid  # Devuelve el ID del producto creado
        except Exception as e:
            print(f"Error al insertar el producto: {e}")
            conn.rollback()  # Rollback en caso de error
        finally:
            cursor.close()
            conn.close()


    @staticmethod
    def get_all_products():
        conn = conectar()
        cursor = conn.cursor()
        query = "SELECT idProducto, Nombre, Descripcion, Imagen, Precio FROM PRODUCTO"
        cursor.execute(query)
        productos = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return [
            {
                'idProducto': producto[0],
                'Nombre': producto[1],
                'Descripcion': producto[2],
                'Precio': producto[4],  # Cambié el índice a 4 porque el precio está en la columna 5 (índice 4)
                'Imagen': base64.b64encode(producto[3]).decode('utf-8') if producto[3] else None  # La imagen está en la columna 4 (índice 3)
            }
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
    @staticmethod
    def get_products_by_service(service_id):
        conn = conectar()
        cursor = conn.cursor()
        query = """
            SELECT p.idProducto, p.Nombre, p.Descripcion, p.Precio
            FROM PRODUCTO p
            INNER JOIN ServicioProducto sp ON p.idProducto = sp.idProducto
            WHERE sp.idServicio = %s
        """
        cursor.execute(query, (service_id,))
        productos = cursor.fetchall()
        cursor.close()
        conn.close()

        return [
            {'idProducto': producto[0], 'Nombre': producto[1], 'Descripcion': producto[2], 'Precio': producto[3]}
            for producto in productos
        ]
