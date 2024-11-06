# En el archivo de rutas o en el controlador del empleado
from flask import Blueprint, render_template, request, redirect, url_for, session
from app.Models.Cita import Cita
from app.Models.Empleado import Empleado
empleado_bp = Blueprint('empleado', __name__, url_prefix='/empleado')

@empleado_bp.route('/citas', methods=['GET'])
def citas():
   
    id_usuario = session.get('user_id')
    if not id_usuario:
        return redirect(url_for('auth.login'))

    id_empleado=Empleado.get_empleado_id_by_id_user(id_usuario)
    citas = Cita.get_citas_by_idEmpleado(id_empleado)
    return render_template('empleado/citas.html', citas=citas)
