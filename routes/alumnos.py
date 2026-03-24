from flask import Blueprint, render_template
from database.databases import PostgreSQL

# Definimos el blueprint
students_bp = Blueprint('alumnos', __name__)

# Instancia de la Base de datos (Operaciones)
pg = PostgreSQL()

@students_bp.get("/")
def index():
    return render_template(
        'global_stats.html', 
        title="Listado de Alumnos",
        context="Alumnos"
    )