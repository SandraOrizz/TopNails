from flask import Blueprint, render_template, request, redirect, url_for, session
from app.Models.Cita import Cita
from app.Models.Empleado import Empleado
from app.Models.Estado import Estado

empleado_bp = Blueprint('empleado', __name__, url_prefix='/empleado')

# Ruta para mostrar las citas asignadas
@empleado_bp.route('/citas', methods=['GET'])
def citas():
    id_usuario = session.get('user_id')
    if not id_usuario:
        return redirect(url_for('auth.login'))

    id_empleado = Empleado.get_empleado_id_by_id_user(id_usuario)
    citas = Cita.get_citas_by_idEmpleado(id_empleado)

    # Obtener todos los estados disponibles
    estados = Estado.get_all_estados()

    return render_template('empleado/citas.html', citas=citas, estados=estados)


@empleado_bp.route('/actualizar_estado', methods=['POST'])
def actualizar_estado():
    id_usuario = session.get('user_id')
    if not id_usuario:
        return redirect(url_for('auth.login'))

    id_empleado = Empleado.get_empleado_id_by_id_user(id_usuario)
    
    # Iterar sobre todas las citas para actualizar el estado
    for cita in Cita.get_citas_by_idEmpleado(id_empleado):
        # Cambiar cita.CitaID a cita['CitaID']
        estado_id = request.form.get(f"estado_{cita['CitaID']}")
        if estado_id:
            Cita.actualizar_estado(cita['CitaID'], estado_id)

    return redirect(url_for('empleado.citas'))
