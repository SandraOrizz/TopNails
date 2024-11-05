from datetime import datetime, timedelta
from app.db import conectar

class Cita:
    @staticmethod
    def create_appointment(client_id, service_id, product_id, state_id, datetime_obj, price):
        # Calcula la hora de fin sumando 2 horas al inicio
        end_time = datetime_obj + timedelta(hours=2)

        # Encuentra un empleado disponible en el horario solicitado
        employee_id = Cita.find_available_employee(datetime_obj, end_time)
        if not employee_id:
            raise Exception("No hay empleados disponibles en ese horario.")

        conn = conectar()
        cursor = conn.cursor()
        query = """
        INSERT INTO CITA (idCliente, idServicio, idEstado, idProducto, idEmpleado, FechaCita, SesionInicio, SesionFin, Precio)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            client_id, service_id, state_id, product_id, employee_id, 
            datetime_obj.date(), datetime_obj.time(), end_time.time(), price
        ))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def find_available_employee(start_time, end_time):
        conn = conectar()
        cursor = conn.cursor()
        query = """
        SELECT idEmpleado FROM EMPLEADO
        WHERE idEmpleado NOT IN (
            SELECT idEmpleado FROM CITA
            WHERE (SesionInicio < %s AND SesionFin > %s)
        )
        LIMIT 1
        """
        cursor.execute(query, (end_time, start_time))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result[0] if result else None

    @staticmethod
    def check_availability(employee_id, start_time, end_time):
        conn = conectar()
        cursor = conn.cursor()
        query = """
        SELECT COUNT(*) FROM CITA
        WHERE idEmpleado = %s AND 
        (
            (SesionInicio < %s AND SesionFin > %s) OR 
            (SesionInicio < %s AND SesionFin > %s) OR 
            (SesionInicio >= %s AND SesionFin <= %s)
        )
        """
        cursor.execute(query, (employee_id, end_time, start_time, start_time, start_time, start_time, end_time))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result[0] == 0
    @staticmethod
    def get_appointments_by_client(client_id):
        print("cliente id:")
        print(client_id)
        conn = conectar()
        cursor = conn.cursor()
        query = """
        SELECT C.idCita, S.Nombre AS Servicio, P.Nombre AS Producto, 
            E.Descripcion AS Estado, C.FechaCita, C.SesionInicio, 
            C.SesionFin, C.Precio
        FROM CITA C
        JOIN SERVICIO S ON C.idServicio = S.idServicio
        JOIN PRODUCTO P ON C.idProducto = P.idProducto
        JOIN ESTADO E ON C.idEstado = E.idEstado
        WHERE C.idCliente = %s
        ORDER BY C.FechaCita DESC
        """
        cursor.execute(query, (client_id,))
        appointments = cursor.fetchall()
        cursor.close()
        conn.close()
        return [
        {
            'idCita': row[0],
            'Servicio': row[1],
            'Producto': row[2],
            'Estado': row[3],
            'FechaCita': row[4],
            'SesionInicio': row[5],
            'SesionFin': row[6],
            'Precio': row[7]
        }
        for row in appointments
    ]
        
    @staticmethod
    def get_citas_by_idEmpleado(IdEmpleado):
        conn = conectar()
        cursor = conn.cursor()
        query = """
            SELECT 
                CONCAT(cli_persona.Nombre, ' ', cli_persona.Apellido) AS NombreCliente,
                s.Nombre AS Servicio,
                p.Nombre AS Producto,
                CONCAT(emp_persona.Nombre, ' ', emp_persona.Apellido) AS EmpleadoResponsable,
                c.FechaCita,
                c.SesionInicio,
                c.SesionFin,
                c.Precio
            FROM 
                CITA c
            JOIN 
                CLIENTE cli ON c.idCliente = cli.idCliente
            JOIN 
                PERSONA cli_persona ON cli.idPersona = cli_persona.idPersona
            JOIN 
                SERVICIO s ON c.idServicio = s.idServicio
            JOIN 
                PRODUCTO p ON c.idProducto = p.idProducto
            JOIN 
                EMPLEADO e ON c.idEmpleado = e.idEmpleado
            JOIN 
                PERSONA emp_persona ON e.idPersona = emp_persona.idPersona
            JOIN 
                ESTADO est ON c.idEstado = est.idEstado
            WHERE 
                est.Descripcion = 'Pendiente' AND e.idEmpleado = %s
        """
        cursor.execute(query, (IdEmpleado,)) 
        citas = cursor.fetchall()
        cursor.close()
        conn.close()
        return [
            {
                'NombreCliente': row[0],
                'Servicio': row[1],
                'Producto': row[2],
                'EmpleadoResponsable': row[3],
                'FechaCita': row[4],
                'SesionInicio': row[5],
                'SesionFin': row[6],
                'Precio': row[7]
            }
            for row in citas
        ]
