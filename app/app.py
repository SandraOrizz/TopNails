from flask import Flask
from app.db import conectar
from app.routers import auth_routes, dashboard_routes, other_routes, admin_routes  ,client_routes,employee_routes

def create_app():
    app = Flask(__name__)
    app.secret_key = 'mi_secreto'

    app.register_blueprint(auth_routes.bp)
    app.register_blueprint(dashboard_routes.bp)
    app.register_blueprint(other_routes.bp)
    app.register_blueprint(admin_routes.bp)  
    app.register_blueprint(client_routes.cliente_bp)
    app.register_blueprint(employee_routes.empleado_bp)
    return app
