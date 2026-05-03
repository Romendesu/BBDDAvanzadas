from flask import (
    Blueprint, request, render_template
)
from models import OperacionesProfesor

profesores_bp = Blueprint('matriculas', __name__, url_prefix="/profesores")

@profesores_bp.route('/')
def home():
    title = "Profesores"
    count_profesores = OperacionesProfesor().get_count()

    return render_template(
        "/home/stats.html",
        title = title,
        n_elements = count_profesores
    )