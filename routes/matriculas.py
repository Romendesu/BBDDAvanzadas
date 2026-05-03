from flask import (
    Blueprint, request, render_template
)

from models import OperacionesMatricula

matriculas_bp = Blueprint('matriculas', __name__, url_prefix="/matriculas")

@matriculas_bp.route('/')
def home():
    title = "Matriculas"
    count_matricula = OperacionesMatricula().get_count()

    return render_template(
        "/home/stats.html",
        title = title,
        n_elements = count_matricula

    )