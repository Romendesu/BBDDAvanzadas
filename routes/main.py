from flask import Blueprint, render_template
from database.databases import PostgreSQL
from routes.response import ResponseJSON
from threading import Lock

# Definimos el blueprint
main_bp = Blueprint('main', __name__)
mutex = Lock()
# Instanciamos la base de datos de manera global
pg = PostgreSQL()

# End-point de inicio
@main_bp.route('/')
def index():
    # Operaciones a la base de datos de manera segura
    global pg
    with mutex:
        stats = pg.count_elm()
        return render_template('index.html', stats=stats)

# End-points para recibir información
@main_bp.route('/obtain-profesores')
def get_teachers():
    global pg
    with mutex:
        try:
            teachers = pg.get_teachers() 
            if teachers:
                teachers_dict = [t.to_dict() for t in teachers]
                return ResponseJSON.ok(str(teachers_dict))
            else:
                return ResponseJSON.no_content()
        except Exception as e:
            return ResponseJSON.error(f"Error: {e}")
        
@main_bp.route('/obtain-alumnos')
def get_students():
    global pg
    with mutex:
        try:
            students = pg.get_students() 
            if students:
                students_dict = [s.to_dict() for s in students]
                return ResponseJSON.ok(str(students_dict))
            else:
                return ResponseJSON.no_content()
        except Exception as e:
            return ResponseJSON.error(f"Error: {e}")
        
@main_bp.route('/obtain-cursos')
def get_grades():
    global pg
    with mutex:
        try:
            grades = pg.get_grades() 
            if grades:
                grades_dict = [g.to_dict() for g in grades]
                return ResponseJSON.ok(str(grades_dict))
            else:
                return ResponseJSON.no_content()
        except Exception as e:
            return ResponseJSON.error(f"Error: {e}")