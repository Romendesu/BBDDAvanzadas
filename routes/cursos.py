from flask import (
    Blueprint, request, render_template
)

cursos_bp = Blueprint('cursos', __name__, url_prefix="/cursos")

@cursos_bp.route('/')
def home():
    title = "Cursos"
    return render_template(
        "/home/stats.html",
        title = title
    )