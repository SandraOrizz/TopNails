from app.db import conectar


class Persona:
    def __init__(self, idPersona, Nombre, Apellido, Cumple, TipoPersonal):
        self.idPersona = idPersona
        self.Nombre = Nombre
        self.Apellido = Apellido
        self.Cumple = Cumple
        self.TipoPersonal = TipoPersonal

    @staticmethod
    def create_persona(Nombre, Apellido, Cumple, TipoPersonal):
        conn = conectar()
        cursor = conn.cursor()
        query = """
        INSERT INTO PERSONA (Nombre, Apellido, Cumple, TipoPersonal)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (Nombre, Apellido, Cumple, TipoPersonal))
        conn.commit()
        persona_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return persona_id

    @staticmethod
    def get_persona_by_id(idPersona):
        conn = conectar()
        cursor = conn.cursor()
        query = "SELECT * FROM PERSONA WHERE idPersona = %s"
        cursor.execute(query, (idPersona,))
        persona = cursor.fetchone()
        cursor.close()
        conn.close()
        return persona
