from flask import Flask
from routes import main_bp, teacher_bp, students_bp, enrollment_bp, grades_bp

# Middlewares + renderizado
def create_app() -> Flask:
    # Instancia de Flask
    app = Flask(__name__)

    # Desactivar el cache
    app.config['TEMPLATES_AUTO_RELOAD'] = True

    # Renderizado de blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(teacher_bp, url_prefix='/profesores')
    app.register_blueprint(students_bp, url_prefix='/alumnos')
    app.register_blueprint(enrollment_bp, url_prefix='/matriculas')
    app.register_blueprint(grades_bp, url_prefix='/cursos')

    # Renderizado de peticiones 4XX (De momento nada)
    return app

# Ejecuccion del programa
def main():
    app = create_app()
    app.run(debug=True)

if __name__ == "__main__":
    main()