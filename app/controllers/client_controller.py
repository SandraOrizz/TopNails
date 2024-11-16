from app.Models.Servicio import Servicio
from app.Models.Producto import Producto
from app.Models.Cita import Cita
from datetime import datetime
from app.db import conectar
class ClientController:

    @staticmethod
    def get_services():
        """Obtiene todos los servicios disponibles."""
        return Servicio.get_all_services()

    @staticmethod
    def get_products():
        """Obtiene todos los productos disponibles."""
        return Producto.get_all_products()

    @staticmethod
    def get_products_by_service(service_id):
        """Obtiene los productos relacionados a un servicio específico."""
        return Producto.get_products_by_service(service_id)

    @staticmethod
    def schedule_appointment(service_id, product_id, date, time, client_id):
        print("Empezando validacion")
        print(service_id)
        print(product_id)
        try:
            # Validar fecha y hora
            appointment_datetime = datetime.strptime(f"{date} {time}", '%Y-%m-%d %H:%M')
            if appointment_datetime < datetime.now():
                print("hora invalida")
                return "La fecha y hora deben ser en el futuro."

            print("hora valida")
          
            price=Producto.get_product_price(product_id)+Servicio.get_service_price(service_id) 
            state_id=1

            print("validado")
            
            # Llamada a la función create_appointment con el orden correcto de los parámetros
            result = Cita.create_appointment(client_id, service_id, product_id, state_id, appointment_datetime, price)
            
            print(result)
            if result==True:
                print("Cita programada")
                return "Cita programada exitosamente."
            else:
                return "No se pudo agendar la cita."
        except Exception as e:
            return f"Error al agendar la cita: {str(e)}"


    @staticmethod
    def get_client_appointments(cliente_id):
        """Obtiene todas las citas del cliente."""
        return Cita.get_appointments_by_cliente(cliente_id)
    @staticmethod
    def get_client_appointments(cliente_id):
        """
        Recupera las citas de un cliente.
        """
        try:
            # Aquí asumimos que usas algún ORM o consultas SQL directas.
            conn = conectar()  # Método para conectar a la base de datos
            cursor = conn.cursor()
            query = """
            SELECT 
                C.Idcita, 
                C.FechaCita, 
                C.SesionInicio, 
                C.SesionFin, 
                C.Precio, 
                P.Nombre AS EmpleadoNombre, 
                P.Apellido AS EmpleadoApellido, 
                S.Descripcion AS ServicioDescripcion, 
                PR.Nombre AS ProductoNombre, 
                ES.Descripcion AS EstadoCita
            FROM 
                CITA C
            JOIN 
                SERVICIO S ON C.idServicio = S.idServicio
            JOIN 
                PRODUCTO PR ON C.idProducto = PR.idProducto
            JOIN 
                ESTADO ES ON C.idEstado = ES.idEstado
            JOIN 
                EMPLEADO E ON C.idEmpleado = E.idEmpleado
            JOIN 
                PERSONA P ON E.idPersona = P.idPersona
            WHERE 
                C.idCliente = %s
            """
            cursor.execute(query, (cliente_id,))
            citas = cursor.fetchall()
            cursor.close()
            conn.close()

            # Retorna las citas obtenidas.
            return citas
        except Exception as e:
            print(f"Error al obtener citas: {str(e)}")
            return []
