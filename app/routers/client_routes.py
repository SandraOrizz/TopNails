from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from app.controllers.client_controller import ClientController
from app.Models.Cliente import Cliente

cliente_bp = Blueprint('client', __name__, url_prefix='/client')

@cliente_bp.route('/services', methods=['GET'])
def view_services():
    try:
        services = ClientController.get_services()
        return render_template('cliente/services.html', services=services)
    except Exception as e:
        return render_template('cliente/error.html', message=f"Error al cargar servicios: {str(e)}")
    
@cliente_bp.route('/productos', methods=['GET'])
def view_productos():
    try:
        product = ClientController.get_products()
        return render_template('cliente/productos.html', products=product)
    except Exception as e:
        return render_template('cliente/productos.html', message=f"Error al cargar productos: {str(e)}")





@cliente_bp.route('/schedule', methods=['POST', 'GET'])
def schedule_appointment():
    if request.method == 'POST':
        try:
            service_id = request.form['service_id']
            product_id = request.form['product_id']
            date = request.form['date']
            time = request.form['time']
            user_id = session.get('user_id')
            
            if not user_id:
                return redirect(url_for('auth.login'))
            
            client_id = Cliente.get_cliente_id_by_user_id(user_id)
            if not client_id:
                return redirect(url_for('auth.login'))

            result = ClientController.schedule_appointment(service_id, product_id, date, time, client_id)
            if result == "Cita programada exitosamente.":
                print("entra en el if 1")
                return redirect(url_for('auth.client_home'))
            else:
                print("error 1")
                return render_template('cliente/error.html', message=result)
        except Exception as e:
            print("error 2")
            return render_template('cliente/error.html', message=f"Error al agendar cita: {str(e)}")
    else:
        try:
            services = ClientController.get_services()
            products = ClientController.get_products()
            return render_template('cliente/schedule.html', services=services, products=products)
        except Exception as e:
            print("error 4")
            return render_template('cliente/error.html', message=f"Error al cargar el formulario: {str(e)}")

@cliente_bp.route('/appointments', methods=['GET'])
def view_appointments():
    try:
        user_id = session.get('user_id')
        if not user_id:
            return redirect(url_for('auth.login'))
        
        cliente_id = Cliente.get_cliente_id_by_user_id(user_id)
        if not cliente_id:
            return render_template('cliente/error.html', message="Cliente no encontrado")
        
        citas = ClientController.get_client_appointments(cliente_id)
        return render_template('cliente/appointments.html', citas=citas)
    except Exception as e:
        return render_template('cliente/error.html', message=f"Error al cargar citas: {str(e)}")

@cliente_bp.route('/get_products/<int:service_id>', methods=['GET'])
def get_products_for_service(service_id):
    try:
        products = ClientController.get_products_by_service(service_id)
        return jsonify(products)
    except Exception as e:
        return jsonify({'error': f"Error al obtener productos: {str(e)}"}), 400
