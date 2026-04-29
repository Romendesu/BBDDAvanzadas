from flask import (
    Blueprint, request, render_template
)

cursos_bp = Blueprint('cursos', __name__, url_prefix="/cursos")

@cursos_bp.route('/', methods=('GET', 'POST'))
def home():
    match request.method:
        case "GET":
            title = "Cursos"
            return f"<p> Renderizado la vista de {title}</p>"
        
        case "_":
            return f"<p> Aun no se ha definido el comportamiento para el metodo {request.method}</p>"
        
