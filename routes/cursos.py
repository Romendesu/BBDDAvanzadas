from flask import Blueprint, render_template
from database.databases import PostgreSQL

# Definimos el blueprint
grades_bp = Blueprint('cursos', __name__)

# Instancia de la Base de datos (Operaciones)
pg = PostgreSQL()

@grades_bp.get("/")
def index():
    return render_template(
        'global_stats.html', 
        title="Listado de Cursos",
        context="Cursos"
    )