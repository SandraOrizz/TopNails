from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from  app.controllers.auth_controler import AuthController
from app.Models.Usuario import Usuario
bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role_id = request.form['role']

        persona_id = AuthController.login_user(username, password, role_id)  # Captura el idPersona
        if persona_id:  # Si el inicio de sesión fue exitoso
            session['persona_id'] = persona_id  # (Ya se guarda en AuthController, pero aquí está por si acaso)
            # Redirigir según el rol
            if role_id == '1':  # Administrador
                return redirect(url_for('auth.admin_home'))
            elif role_id == '2':  # Cliente
                return redirect(url_for('auth.client_home'))
            elif role_id == '3':  # Empleado
                return redirect(url_for('auth.employee_home'))
        else:
            flash("Usuario o contraseña incorrectos", "error")
            return redirect(url_for('auth.login'))

    return render_template('login.html')

@bp.route('/admin_home')
def admin_home():
    return render_template('admin_home.html')  # Página de inicio para el administrador

@bp.route('/client_home')
def client_home():
    return render_template('client_home.html')  # Página de inicio para el cliente

@bp.route('/employee_home')
def employee_home():
    return render_template('employee_home.html')  # Página de inicio para el empleado

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        result = AuthController.register_user(username, password)
        if result == True:
            return redirect(url_for('auth.login'))
        else:
            return result

    return render_template('register.html')

@bp.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('role', None)
    return redirect(url_for('auth.login'))

@bp.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if request.method == 'POST':
        user_id = session.get('user_id')
        current_password = request.form['current_password']
        new_password = request.form['new_password']

        username = Usuario.get_username_by_id(user_id)
        if not username:
            return redirect(url_for('auth.login'))

        # Cambiar la contraseña usando el controlador de autenticación
        result = AuthController.change_password(username, current_password, new_password)
        
        if result == "Contraseña actualizada correctamente":
            # Eliminar los datos de sesión
            session.pop('user_id', None)
            session.pop('persona_id', None)
            session.pop('role', None)
            flash("Contraseña actualizada correctamente. Por favor, vuelve a iniciar sesión.", "success")
            return redirect(url_for('auth.login'))
        else:
            flash(result, "error")

    return render_template('change_password.html')
