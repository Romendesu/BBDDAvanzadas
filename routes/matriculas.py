from flask import (
    Blueprint, request, render_template
)

matriculas_bp = Blueprint('matriculas', __name__, url_prefix="/matriculas")

@matriculas_bp.route('/', methods=('GET', 'POST'))
def home():
    match request.method:
        case "GET":
            title = "matriculas"
            return f"<p> Renderizado la vista de {title}</p>"
        
        case "_":
            return f"<p> Aun no se ha definido el comportamiento para el metodo {request.method}</p>"
        
