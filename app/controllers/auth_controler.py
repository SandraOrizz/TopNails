# controllers/auth_controller.py

from flask import session
import hashlib
from app.Models.Usuario import Usuario

class AuthController:
    @staticmethod
    def login_user(username, password, role_id):
        # Hashear la contraseña antes de buscar
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        user = Usuario.find_user_by_credentials(username, hashed_password)

        if user:
            # Verifica los roles del usuario
            roles = Usuario.get_roles_by_user(user['idUsuario'])

            # Convertir role_id a entero si es de tipo str
            if isinstance(role_id, str):
                try:
                    role_id = int(role_id)  # Convertir a entero
                except ValueError:
                    print("role_id no se puede convertir a entero:", role_id)
                    return False  # Manejar el error devolviendo False

            # Asegúrate de que roles contenga enteros
            roles = [int(role) for role in roles]  # Convertir roles a enteros

            # Verificar si role_id está en roles
            if role_id in roles:
                session['user_id'] = user['idUsuario']
                session['persona_id'] = user['idPersona']  # Guarda el idPersona en la sesión
                session['roles'] = roles  # Guardar roles en la sesión
                session['role'] = role_id   # Almacena el rol seleccionado en la sesión

                return user['idPersona']  # Devuelve el idPersona
            else:
                print("Rol no autorizado")
                return False  # Rol no autorizado

        return False  # Usuario no encontrado

    @staticmethod
    def register_user(username, password):
        try:
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            Usuario.create_user(username, hashed_password)
            return True
        except Exception as e:
            return f"Error: {e}"

    @staticmethod
    def change_password(username, current_password, new_password):
        
        hashed_current_password = hashlib.sha256(current_password.encode()).hexdigest()
        user = Usuario.find_user_by_credentials(username, hashed_current_password)
        if user:
            hashed_new_password = hashlib.sha256(new_password.encode()).hexdigest()
            Usuario.update_password(username, hashed_new_password)
            return"Contraseña actualizada correctamente"
        return "La contraseña actual no es correcta"
