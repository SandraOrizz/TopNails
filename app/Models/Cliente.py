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
    