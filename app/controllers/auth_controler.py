# controllers/auth_controller.py

from  app.Models.User_model import UserModel

class AuthController:
    @staticmethod
    def login_user(username, password):
        user = UserModel.find_user_by_credentials(username, password)
        if user:
            return True
        return False

    @staticmethod
    def register_user(username, password):
        try:
            UserModel.create_user(username, password)
            return True
        except Exception as e:
            return f"Error: {e}"

    @staticmethod
    def change_password(username, current_password, new_password):
        # Verificar la contraseña actual
        user = UserModel.find_user_by_credentials(username, current_password)
        if user:
            UserModel.update_password(username, new_password)
            return "Contraseña actualizada correctamente"
        return "La contraseña actual no es correcta"
