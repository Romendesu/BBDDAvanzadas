from flask import (
    Blueprint, request, render_template
)
from models import OperacionesAlumno


alumnos_bp = Blueprint('students', __name__, url_prefix="/alumnos")

@alumnos_bp.route('/')
def home():
    title = "Alumnos"
    return render_template(
        "/home/stats.html",
        title = title
    )