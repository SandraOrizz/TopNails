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

    
    @staticmethod
    def get_empleado_id_by_id_user(idUser):
        conn=conectar()
        cursor=conn.cursor()
        query="SELECT e.idEmpleado FROM USUARIO u JOIN  PERSONA p ON u.idPersona = p.idPersona JOIN   EMPLEADO e ON p.idPersona = e.idPersona WHERE u.idUsuario = %s "
        cursor.execute(query,(idUser,))
        idEmpleado=cursor.fetchone()
        cursor.close()
        conn.close()
        return idEmpleado[0] if idEmpleado else None 