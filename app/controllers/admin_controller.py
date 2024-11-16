from flask import session, request, flash, redirect, url_for
from app.Models.Persona import Persona
from app.Models.Usuario import Usuario
from app.Models.Cliente import Cliente
from app.Models.Empleado import Empleado
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
                if not Cliente.create_cliente(persona_id):
                    flash("Error al crear cliente", "error")
                    return False

            # Si el rol es Empleado, crear un registro en la tabla EMPLEADO
            if role_id == '3':  # ID del rol de Empleado
                if not Empleado.create_employee(persona_id):
                    flash("Error al crear empleado", "error")
                    return False

            # Crear el nombre de usuario: primera letra del nombre + apellido
            username = first_name[0].lower() + last_name.lower()

            # Crear usuario asignado a esa persona
            hashed_password = hashlib.sha256(user_data['password'].encode()).hexdigest()
            user_data['password'] = hashed_password
            user_data['username'] = username
            user_data['idPersona'] = persona_id
            user_data['role'] = role_id

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
    def insert_producto(nombre, descripcion, precio):
        try:
            # Llama al método create_producto para insertar el producto en la base de datos
            if Producto.create_producto(nombre, descripcion, precio):
                flash("Producto creado con éxito", "success")
                return True
            else:
                flash("Error al crear producto", "error")
                return False
        except Exception as e:
            print(f"Error en insert_producto: {str(e)}")
            flash("Ocurrió un error al intentar crear el producto.", "error")
            return False

    @staticmethod
    def insert_servicio(nombre, descripcion, costo, productos_seleccionados):
        try:
            # Crear el servicio
            servicio_id = Servicio.create_servicio(nombre, descripcion, costo)
            if not servicio_id:
                flash("Error al crear servicio", "error")
                return False

            # Asociar productos con el servicio
            for producto_id in productos_seleccionados:
                if not Servicio.add_product_to_service(servicio_id, producto_id):
                    flash("Error al asociar producto con el servicio", "error")
                    return False

            flash("Servicio creado con éxito", "success")
            return True

        except Exception as e:
            print(f"Error en insert_servicio: {str(e)}")
            flash("Ocurrió un error al intentar crear el servicio.", "error")
            return False