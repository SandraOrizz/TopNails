from app.db import conectar

class Cliente:
    @staticmethod
    def create_cliente(id_persona):
        conn = conectar()
        cursor = conn.cursor()
        query = """
        INSERT INTO CLIENTE (idPersona, Puntos)
        VALUES (%s, 0)
        """
        cursor.execute(query, (id_persona,))
        conn.commit()
        cliente_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return cliente_id

    @staticmethod
    def get_cliente_id_by_user_id(user_id):
        conn = conectar()
        cursor = conn.cursor()
        query = """
        SELECT C.idCliente 
        FROM CLIENTE C
        INNER JOIN USUARIO U ON C.idPersona = U.idPersona 
        WHERE U.idUsuario = %s
        """
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()

        if result:
            return result[0]  # Retorna el idCliente si se encuentra
        return None  # Retorna None si no se encuentra
