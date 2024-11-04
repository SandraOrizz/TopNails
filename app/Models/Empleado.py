from app.db import conectar

class Empleado:
    @staticmethod
    def create_employee(id_persona, salario=3000000):
        conn = conectar()
        cursor = conn.cursor()
        query = """
        INSERT INTO EMPLEADO (idPersona, Salario,FechaIngreso)
        VALUES (%s, %s,curdate())
        """
        cursor.execute(query, (id_persona, salario))
        conn.commit()
        empleado_id = cursor.lastrowid  # Obtener el ID del empleado recién creado
        cursor.close()
        conn.close()
        return empleado_id  # Devolver el ID del empleado
