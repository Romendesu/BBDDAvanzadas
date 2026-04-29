from flask import (
    Blueprint, request, render_template
)

profesores_bp = Blueprint('matriculas', __name__, url_prefix="/profesores")

@profesores_bp.route('/', methods=('GET', 'POST'))
def home():
    match request.method:
        case "GET":
            title = "profesores"
            return f"<p> Renderizado la vista de {title}</p>"
        
        case "_":
            return f"<p> Aun no se ha definido el comportamiento para el metodo {request.method}</p>"
        
