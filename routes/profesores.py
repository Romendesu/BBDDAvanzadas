from flask import (
    Blueprint, request, render_template
)

profesores_bp = Blueprint('matriculas', __name__, url_prefix="/profesores")

@profesores_bp.route('/')
def home():
    title = "Profesores"
    return render_template(
        "/home/stats.html",
        title = title
    )