from flask import Blueprint, render_template
from database.databases import PostgreSQL

# Definimos el blueprint
teacher_bp = Blueprint('profesores', __name__)

# Instancia de la Base de datos (Operaciones)
pg = PostgreSQL()

@teacher_bp.get("/")
def index():
    return render_template(
        'global_stats.html', 
        title="Listado de Profesores",
        context="Profesores"
    )
