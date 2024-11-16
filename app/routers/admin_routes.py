from flask import Blueprint, render_template, request, redirect, url_for
from app.controllers.admin_controller import AdminController
from app.Models.Producto import Producto
bp = Blueprint('admin', __name__)

@bp.route('/admin/create_user', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        # Obtener los datos de la persona
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        birthdate = request.form['birthdate']  # Obtener la fecha de nacimiento
        role_id = request.form['role']  # ID del rol

        # Generar el nombre de usuario
        username = first_name[0].lower() + last_name.lower()  # Primera letra del nombre + apellido
        
        persona_data = {
            'first_name': first_name,
            'last_name': last_name,
            'birthdate': birthdate,  # Agregar la fecha de nacimiento
        }
        user_data = {
            'username': username,  # Usar el nombre de usuario generado
            'password': request.form['password'],
        }

        if AdminController.insert_user_person(role_id, persona_data, user_data):
            return redirect(url_for('auth.admin_home'))
        else:
            return redirect(url_for('admin.error'))
    
    return render_template('admin/create_user.html')


@bp.route('/admin/create_producto', methods=['GET', 'POST'])
def create_producto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        
        if AdminController.insert_producto(nombre, descripcion, precio):
          
             return redirect(url_for('auth.admin_home'))
        else:
            
            return redirect(url_for('admin.create_producto'))
    
    return render_template('admin/create_producto.html')

@bp.route('/admin/create_servicio', methods=['GET', 'POST'])
def create_servicio():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        costo = request.form['precio']  # Cambia 'precio' a 'costo' para coincidir con insert_servicio

        # Obtener los productos seleccionados
        productos_seleccionados = request.form.getlist('productos')  # 'productos' es el nombre del campo de los productos seleccionados

        if AdminController.insert_servicio(nombre, descripcion, costo, productos_seleccionados):
            return redirect(url_for('auth.admin_home'))
        else:
            return redirect(url_for('admin.create_servicio'))
    
    # Obtener todos los productos disponibles para mostrarlos en el formulario
    productos = Producto.get_all_products()  # Este método debe devolver todos los productos
    return render_template('admin/create_servicio.html', productos=productos)
