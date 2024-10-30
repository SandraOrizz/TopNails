from app.db import conectar
import hashlib

class UserModel:
    @staticmethod
    def find_user_by_credentials(username, password):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        conn = conectar()
        cursor = conn.cursor()
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        cursor.execute(query, (username, hashed_password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        return user

    @staticmethod
    def create_user(username, password):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        conn = conectar()
        cursor = conn.cursor()
        query = "INSERT INTO users (username, password) VALUES (%s, %s)"
        cursor.execute(query, (username, hashed_password))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def update_password(username, new_password):
        hashed_new_password = hashlib.sha256(new_password.encode()).hexdigest()
        conn = conectar()
        cursor = conn.cursor()
        query = "UPDATE users SET password = %s WHERE username = %s"
        cursor.execute(query, (hashed_new_password, username))
        conn.commit()
        cursor.close()
        conn.close()
