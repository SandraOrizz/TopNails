# models/user_model.py

import hashlib
from app.db import conectar

class Usuario:
    @staticmethod
    def find_user_by_credentials(username, hashed_password):
        conn = conectar()
        cursor = conn.cursor()
        query = "SELECT idUsuario, idPersona FROM USUARIO WHERE UserName = %s AND Clave = %s"
        cursor.execute(query, (username, hashed_password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        if user:
            return {'idUsuario': user[0], 'idPersona': user[1]}
        return None

    @staticmethod
    def create_user(username, hashed_password):
        conn = conectar()
        cursor = conn.cursor()
        query = "INSERT INTO USUARIO (UserName, Clave, Estado) VALUES (%s, %s, 1)"
        cursor.execute(query, (username, hashed_password))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def update_password(username, hashed_password):
        conn = conectar()
        cursor = conn.cursor()
        query = "UPDATE USUARIO SET Clave = %s WHERE UserName = %s"
        cursor.execute(query, (hashed_password, username))
        conn.commit()
        cursor.close()
        conn.close()
    @staticmethod
    def get_roles_by_user(user_id):
 
        print(user_id)
        
        conn = conectar()
        cursor = conn.cursor()
        
        # Realiza la consulta para obtener roles del usuario
        query = "SELECT idROl FROM rolusuario WHERE idUsuario = %s"
        cursor.execute(query, (user_id,))
        
        # Obtiene todos los resultados
        result = cursor.fetchall()  # Usa fetchall() para obtener todos los registros
        
        # Verifica si hay resultados
        if not result:
            print("No se encontraron roles para el usuario con ID:", user_id)
            return []  # Devuelve una lista vacía si no hay roles

        # Imprime los resultados para ver qué se obtuvo
     
        # Devuelve una lista de IDs de rol
        print(row[0] for row in result)
        return [row[0] for row in result]   # Asegúrate de que 'idrol' esté correctamente referenciado
