from flask import (
    Blueprint, request, render_template
)

home_bp = Blueprint('home', __name__, url_prefix="/home")

@home_bp.route('/', methods=('GET', 'POST'))
def home():
    match request.method:
        case "GET":
            return "<p> La aplicación está corriendo perfectamente </p>"
        case "_":
            return f"<p> Aun no se ha definido el comportamiento para el metodo {request.method}</p>"