from flask import (
    Blueprint, request, render_template
)
from models import OperacionesAlumno, OperacionesCurso, OperacionesMatricula, OperacionesProfesor

tabla_alumno = OperacionesAlumno()
tabla_profesor = OperacionesProfesor()
tabla_curso = OperacionesCurso()
tabla_matricula = OperacionesMatricula()

home_bp = Blueprint('home', __name__, url_prefix="/home")

@home_bp.route('/')
def home():
    global tabla_alumno

    title = "Inicio"
    count_alumnos = 0 if not tabla_alumno.get_count() else tabla_alumno.get_count()
    count_profesores = 0 if not tabla_profesor.get_count() else tabla_profesor.get_count()
    count_curso = 0 if not tabla_curso.get_count() else tabla_curso.get_count()
    count_matricula = 0 if not tabla_matricula.get_count() else tabla_matricula.get_count()

    return render_template(
        "/home/home.html", 
        title = title, 
        n_alumnos = count_alumnos, 
        n_profesores = count_profesores,
        n_cursos = count_curso,
        n_matriculas = count_matricula
    )
