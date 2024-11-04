from datetime import datetime
from app.Models.Cliente import Cliente
from app.Models.Servicio import Servicio
from app.Models.Producto import Producto
from app.Models.Cita import Cita
from flask import session

class ClientController:
    @staticmethod
    def get_services():
        return Servicio.get_all_services()

    @staticmethod
    def get_products():
        return Producto.get_all_products()

    @staticmethod
    def schedule_appointment(service_id, product_id, date, time):
        user_id = session.get('user_id')
        client_id = Cliente.get_cliente_id_by_user_id(user_id)
        print("Cliente id")
        print(client_id)
        if client_id is None:
            return "Error: Cliente no encontrado."

        # Obtiene el estado inicial de la cita (por ejemplo, "pendiente")
        initial_state = 1  # Suponiendo que 1 es el id del estado "pendiente"

        # Obtener precios del servicio y del producto
        service_price = Servicio.get_service_price(service_id)
        product_price = Producto.get_product_price(product_id)

        # Calcular el precio total
        total_price = service_price + product_price
        print(total_price)

        # Convertir `date` y `time` a objetos datetime
        try:
            date_obj = datetime.strptime(date, "%Y-%m-%d").date()  # Convierte la fecha a `datetime.date`
            time_obj = datetime.strptime(time, "%H:%M").time()     # Convierte la hora a `datetime.time`
            datetime_obj = datetime.combine(date_obj, time_obj)    # Combina para crear `datetime`

            # Crear la cita
            Cita.create_appointment(client_id, service_id, product_id, initial_state, datetime_obj, total_price)
            return "Cita programada exitosamente."
        except Exception as e:
            return f"Error al programar la cita: {e}"

    @staticmethod
    def get_client_appointments(client_id):
        return Cita.get_appointments_by_client(client_id)
