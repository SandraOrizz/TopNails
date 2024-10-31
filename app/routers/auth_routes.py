# auth_routes.py

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.controllers.auth_controler import AuthController

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role_id = request.form['role']  # Obtén el rol seleccionado

        if AuthController.login_user(username, password, role_id):  # Pasar role_id a la función
            session['username'] = username
            session['role'] = role_id  # Guardar el rol en la sesión
            return redirect(url_for('dashboard.dashboard'))
        else:
            print(password)
            return "Usuario o contraseña incorrectos"

    return render_template('login.html')

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
    session.pop('role', None)  # Asegúrate de eliminar el rol de la sesión también
    return redirect(url_for('auth.login'))

@bp.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if request.method == 'POST':
        username = session.get('username')
        current_password = request.form['current_password']
        new_password = request.form['new_password']

        if not username:
            return redirect(url_for('auth.login'))

        result = AuthController.change_password(username, current_password, new_password)
        if result == "Contraseña actualizada correctamente":
            return redirect(url_for('dashboard.dashboard'))  # Cambia según tu ruta
        else:
            flash(result, "error")  # Mensaje de error

    return render_template('change_password.html')
