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
            # Obtener los datos de la persona
            first_name = persona_data['first_name']
            last_name = persona_data['last_name']
            birthdate = persona_data['birthdate']  # Este debe ser agregado en el formulario

            # Crear nueva persona en la base de datos
            persona_id = Persona.create_persona(first_name, last_name, birthdate)
            if not persona_id:
                flash("Error al crear persona", "error")
                return False

            # Crear el usuario con nombre de usuario y contraseña
            hashed_password = hashlib.sha256(user_data['password'].encode()).hexdigest()
            user_data['password'] = hashed_password
            user_data['username'] = first_name[0].lower() + last_name.lower()  # Crear el nombre de usuario
            user_data['idPersona'] = persona_id
            user_data['role'] = role_id

            # Crear el usuario en la base de datos
            user_id = Usuario.create_user(user_data)
            if not user_id:
                flash("Error al crear usuario", "error")
                return False

            # Insertar la relación en la tabla rolUsuario
            if not Usuario.assign_role_to_user(user_id, role_id):
                flash("Error al asignar rol al usuario", "error")
                return False

            # Si el rol es Cliente o Empleado, crear también el registro correspondiente
            if role_id == '2':  # Cliente
                if not Cliente.create_cliente(persona_id):
                    flash("Error al crear cliente", "error")
                    return False
            elif role_id == '3':  # Empleado
                if not Empleado.create_employee(persona_id):
                    flash("Error al crear empleado", "error")
                    return False

            return True

        except Exception as e:
            print(f"Error en insert_user_person: {str(e)}")
            flash("Ocurrió un error inesperado, por favor inténtelo de nuevo.", "error")
            return False

    @staticmethod
    def insert_producto(nombre, descripcion, precio, imagen=None):
        try:
            # Llama al método create_producto para insertar el producto en la base de datos
            producto_id = Producto.create_producto(nombre, descripcion, precio, imagen)
            if producto_id:
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
    def insert_servicio(nombre, descripcion, precio, productos_seleccionados, imagen=None):
        try:
            # Crear el servicio (insertar servicio sin imagen)
            servicio_id = Servicio.create_servicio(nombre, descripcion, precio, imagen)
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
