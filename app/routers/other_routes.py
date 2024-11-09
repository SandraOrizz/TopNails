from flask import Blueprint, render_template

bp = Blueprint('other', __name__)

@bp.route('/')
def home():
    return render_template('login.html')

@bp.route('/index')
def index():
    return render_template('index.html')

@bp.route('/logoff')
def reservas():
    return render_template('reservas.html')

@bp.route('/disenios')
def disenios():
    return render_template('disenios.html')


