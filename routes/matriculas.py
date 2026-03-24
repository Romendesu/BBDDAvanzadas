from flask import Blueprint, render_template
from database.databases import PostgreSQL

# Definimos el blueprint
enrollment_bp = Blueprint('matriculas', __name__)

# Instancia de la Base de datos (Operaciones)
pg = PostgreSQL()

@enrollment_bp.get("/")
def index():
    return render_template(
        'global_stats.html', 
        title="Listado de Matrículas",
        context="Matrículas"
    )