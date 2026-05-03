from flask import (
    Blueprint, request, render_template
)

from models import OperacionesCurso

cursos_bp = Blueprint('cursos', __name__, url_prefix="/cursos")

@cursos_bp.route('/')
def home():
    title = "Cursos"
    count_curso = OperacionesCurso().get_count()

    return render_template(
        "/home/stats.html",
        title = title,
        n_elements = count_curso,
    )