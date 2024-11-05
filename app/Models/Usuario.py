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
    def get_username_by_id(id_User):
        conn = conectar()
        cursor = conn.cursor()
        query = "SELECT username FROM USUARIO WHERE idusuario = %s"
        cursor.execute(query, (id_User,))  # Correcto: la coma crea una tupla de un solo elemento
        username = cursor.fetchone()  # Usar fetchone() para obtener un solo resultado
        cursor.close()
        conn.close()
        return username[0] if username else None  # Extrae el valor si existe

        
    
    
    @staticmethod
    def create_user(user_data):
        conn = conectar()
        cursor = conn.cursor()
        query = "INSERT INTO USUARIO (UserName, Clave, Estado, idPersona) VALUES (%s, %s, 1, %s)"
        cursor.execute(query, (user_data['username'], user_data['password'], user_data['idPersona']))
        conn.commit()
        user_id = cursor.lastrowid  # Obtener el ID del usuario recién creado
        cursor.close()
        conn.close()
        return user_id  # Devolver el ID del usuario

    @staticmethod
    def update_password(username, hashed_password):
        conn = conectar()
        cursor = conn.cursor()
        query = "UPDATE USUARIO SET Clave = %s WHERE UserName = %s"
        cursor.execute(query, (hashed_password, username))
        conn.commit()
        cursor.close()
        conn.close()
        print("cambio")
        
    @staticmethod
    def get_roles_by_user(user_id):
 
      
        
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
    @staticmethod
    def assign_role_to_user(user_id, role_id):
        conn = conectar()
        cursor = conn.cursor()
        query = "INSERT INTO rolUsuario (idUsuario, idRol) VALUES (%s, %s)"
        cursor.execute(query, (user_id, role_id))
        conn.commit()
        cursor.close()
        conn.close()
        return True  # Asumir que la inserción fue exitosa
