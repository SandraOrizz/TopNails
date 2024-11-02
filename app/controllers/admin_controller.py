from flask import session, request, flash, redirect, url_for
from app.Models.Persona import Persona
from app.Models.Usuario import Usuario
from app.Models.Cliente import Cliente  # Asegúrate de importar el modelo Cliente
from app.Models.Servicio import Servicio
from app.Models.Producto import Producto
import hashlib

class AdminController:
    @staticmethod
    def insert_user_person(role_id, persona_data, user_data):
        try:
            # Obtener el nombre, apellido, fecha de nacimiento y tipo de personal
            first_name = persona_data['first_name']
            last_name = persona_data['last_name']
            birthdate = persona_data['birthdate']  # Este debe ser agregado en el formulario

            # Definir el tipo de persona según el rol
            tipo_personal = {
                '1': 'Administrador',
                '2': 'Cliente',
                '3': 'Empleado'
            }.get(role_id, 'Desconocido')  # Valor por defecto

            # Crear nueva persona en la base de datos
            persona_id = Persona.create_persona(first_name, last_name, birthdate, tipo_personal)
            if not persona_id:
                flash("Error al crear persona", "error")
                return False

            # Si el rol es Cliente, crear un registro en la tabla CLIENTE
            if role_id == '2':  # ID del rol de Cliente
                if not Cliente.create_cliente(persona_id):  # Llama al método para crear cliente
                    flash("Error al crear cliente", "error")
                    return False

            # Crear el nombre de usuario: primera letra del nombre + apellido
            username = first_name[0].lower() + last_name.lower()

            # Crear usuario asignado a esa persona
            hashed_password = hashlib.sha256(user_data['password'].encode()).hexdigest()
            user_data['password'] = hashed_password
            user_data['username'] = username  # Asignar el nombre de usuario
            user_data['idPersona'] = persona_id  # Asignar la relación con Persona
            user_data['role'] = role_id  # Asignar rol

            # Insertar usuario en la base de datos
            user_id = Usuario.create_user(user_data)
            if not user_id:
                flash("Error al crear usuario", "error")
                return False

            # Insertar la relación en la tabla rolUsuario
            if not Usuario.assign_role_to_user(user_id, role_id):
                flash("Error al asignar rol al usuario", "error")
                return False

            return True
            
        except Exception as e:
            # Manejo de errores, mostrando el mensaje de error en el log
            print(f"Error en insert_user_person: {str(e)}")
            flash("Ocurrió un error inesperado, por favor inténtelo de nuevo.", "error")
            return False
        
    @staticmethod  
    def insert_producto(nombre,descripcion,precio):
        return Producto.create_producto(nombre,descripcion,precio)

    @staticmethod
    def insert_servicio(nombre,descripcion,costo):
        return Servicio.create_servicio(nombre,descripcion, costo)