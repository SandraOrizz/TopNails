from flask import Blueprint, render_template, request, redirect, url_for, flash,send_file
from werkzeug.utils import secure_filename
from app.controllers.admin_controller import AdminController
from app.Models.Producto import Producto
from app.Models.Servicio import Servicio
from app.Models.Usuario import Usuario
from app.db import conectar  # Usamos conectar() para la conexión a la base de datos
import io

bp = Blueprint('admin', __name__)

# Ruta para la página principal del administrador
@bp.route('/admin/home')
def admin_home():
    return render_template('admin_home.html')

# Ruta para crear un nuevo usuario
@bp.route('/admin/create_user', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        # Obtener los datos de la persona
        persona_data = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'birthdate': request.form['birthdate'],  # Obtener la fecha de nacimiento
        }
        user_data = {
            'username': request.form['first_name'][0].lower() + request.form['last_name'].lower(),
            'password': request.form['password'],
        }

        role_id = request.form['role']  # ID del rol
        
        # Crear usuario, persona y asignar rol
        if AdminController.insert_user_person(role_id, persona_data, user_data):
            flash("Usuario creado exitosamente", "success")
            return redirect(url_for('admin.admin_home'))
        else:
            flash("Hubo un error al crear el usuario", "error")
            return redirect(url_for('admin.create_user'))
    
    return render_template('admin/create_user.html')

# Ruta para crear un nuevo producto
@bp.route('/admin/create_producto', methods=['GET', 'POST'])
def create_producto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = request.form['precio']

        
        file = request.files.get('imagen')
        if file and file.filename!='':                
            imagen_datos = file.read()  
            tipo = file.mimetype
            print(tipo)
            
        try:
            conn = conectar()  # Usamos conectar() para obtener la conexión
            cursor = conn.cursor()

            # Insertar el producto en la tabla 'producto' con la imagen
            sql_producto = "INSERT INTO producto (nombre, descripcion, precio, imagen) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql_producto, (nombre, descripcion, precio, imagen_datos))
            conn.commit()
            cursor.close()

            flash("Producto creado con éxito", "success")
            return redirect(url_for('admin.admin_home'))  # Redirigir a la página principal de administración
        except Exception as e:
            flash(f"Error al crear el producto: {e}", "error")
            return redirect(url_for('admin.create_producto'))
    
    return render_template('admin/create_producto.html')  # Renderizar el formulario para crear producto

# Ruta para crear un nuevo servicio
@bp.route('/admin/create_servicio', methods=['GET', 'POST'])
def create_servicio():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        imagen = request.files.get('imagen')  # Obtener la imagen del formulario
        productos_seleccionados = request.form.getlist('productos')  # Productos seleccionados

        # Procesar la imagen y convertirla en un flujo de bytes
        imagen_datos = None
        nombre_imagen = None
        if imagen:
            nombre_imagen = secure_filename(imagen.filename)
            imagen_datos = imagen.read()  # Leer la imagen en bytes

        # Conexión a la base de datos para insertar el servicio
        try:
            conn = conectar()  # Usamos conectar() aquí
            cursor = conn.cursor()

            # Insertar el servicio en la tabla 'servicio' con la imagen
            sql_servicio = "INSERT INTO servicio (nombre, descripcion, precio, imagen) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql_servicio, (nombre, descripcion, precio, imagen_datos))
            conn.commit()

            # Asociar los productos seleccionados al servicio
            servicio_id = cursor.lastrowid  # Obtener el ID del servicio recién insertado
            for producto_id in productos_seleccionados:
                sql_asociar_producto = "INSERT INTO servicioproducto (idservicio, idProducto) VALUES (%s, %s)"
                cursor.execute(sql_asociar_producto, (servicio_id, producto_id))
            
            conn.commit()
            cursor.close()

            flash("Servicio creado con éxito", "success")
            return redirect(url_for('admin.admin_home'))
        except Exception as e:
            flash(f"Error al crear el servicio: {e}", "error")
            return redirect(url_for('admin.create_servicio'))
    
    # Obtener todos los productos disponibles para asociarlos al servicio
    productos = Producto.get_all_products()
    return render_template('admin/create_servicio.html', productos=productos)

# Ruta para manejar errores
@bp.route('/admin/error')
def error():
    return render_template('admin/error.html')
