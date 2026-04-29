from flask import (
    Blueprint, request, render_template
)

alumnos_bp = Blueprint('students', __name__, url_prefix="/alumnos")

@alumnos_bp.route('/', methods=('GET', 'POST'))
def home():
    match request.method:
        case "GET":
            title = "Alumnos"
            return f"<p> Renderizado la vista de {title}</p>"
        
        case "_":
            return f"<p> Aun no se ha definido el comportamiento para el metodo {request.method}</p>"
        
