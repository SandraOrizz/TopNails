from flask import Blueprint, render_template, request, redirect, url_for, session
from app.controllers.client_controller import ClientController
from app.Models.Cliente import Cliente
cliente_bp = Blueprint('client', __name__, url_prefix='/client')

@cliente_bp.route('/services', methods=['GET'])
def view_services():
    services = ClientController.get_services()
    return render_template('cliente/services.html', services=services)

@cliente_bp.route('/schedule', methods=['POST', 'GET'])
def schedule_appointment():
    if request.method == 'POST':
        service_id = request.form['service_id']
        product_id = request.form['product_id']
        date = request.form['date']
        time = request.form['time']
        client_id = session.get('user_id')
        
    
        result = ClientController.schedule_appointment(service_id, product_id, date, time)
        print(result)
        if result == "Cita programada exitosamente.":
          return redirect(url_for('auth.client_home'))
        else:
            # Manejo de error: podrías redirigir a una página de error o mostrar un mensaje
            return render_template('cliente/error.html', message=result)
    
    else:
        services = ClientController.get_services()
        products = ClientController.get_products()
        return render_template('cliente/schedule.html', services=services, products=products)
@cliente_bp.route('/appointments', methods=['GET'])
def view_appointments():
    id_user = session.get('user_id')
    cliente_id = Cliente.get_cliente_id_by_user_id(id_user)
    print("ID del Cliente:", cliente_id)  # Debug para verificar el ID obtenido

    # Obtenemos las citas del cliente
    citas = ClientController.get_client_appointments(cliente_id)

    print(citas)
    # Renderizamos el template con las citas obtenidas
    return render_template('cliente/appointments.html', citas=citas)
