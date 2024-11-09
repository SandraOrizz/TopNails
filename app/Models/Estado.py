from app.db import conectar

class Estado:
    def __init__(self, idEstado, Descripcion):
        self.idEstado = idEstado
        self.Descripcion = Descripcion

    # Método para crear un nuevo estado
    @staticmethod
    def create_estado(Descripcion):
        conn = conectar()
        cursor = conn.cursor()
        query = """
        INSERT INTO ESTADO (Descripcion)
        VALUES (%s)
        """
        cursor.execute(query, (Descripcion,))
        conn.commit()
        estado_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return estado_id

    # Método para obtener todos los estados
    @staticmethod
    def get_all_estados():
        conn = conectar()
        cursor = conn.cursor()
        query = "SELECT idEstado, Descripcion FROM ESTADO"
        cursor.execute(query)
        rows = cursor.fetchall()  # obtenemos todas las filas
        estados = []
        for row in rows:
            # Cambiamos el acceso con índices a acceso por nombre (diccionario)
            estados.append(Estado(row[0], row[1]))  # Acceso por índice
        cursor.close()
        conn.close()
        return estados

    @staticmethod
    def get_estado_by_id(estado_id):
        conn = conectar()
        cursor = conn.cursor()
        query = "SELECT idEstado, Descripcion FROM ESTADO WHERE idEstado = %s"
        cursor.execute(query, (estado_id,))
        row = cursor.fetchone()  # obtenemos una sola fila
        cursor.close()
        conn.close()
        if row:
            # Acceso por índice ya que 'row' es una tupla
            return Estado(row[0], row[1])
        return None
