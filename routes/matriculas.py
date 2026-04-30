from flask import (
    Blueprint, request, render_template
)

matriculas_bp = Blueprint('matriculas', __name__, url_prefix="/matriculas")

@matriculas_bp.route('/')
def home():
    title = "Matriculas"
    return render_template(
        "/home/stats.html",
        title = title

    )