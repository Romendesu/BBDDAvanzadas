from flask import Flask, redirect, url_for

from config import SERVER_IP, SERVER_PORT, TEMPLATE_DIR
from routes import *

def create_app() -> Flask:
    app = Flask(__name__, template_folder=TEMPLATE_DIR)

    # Registro de blueprints
    app.register_blueprint(alumnos_bp, name = "alumnos")
    app.register_blueprint(cursos_bp, name = "cursos")
    app.register_blueprint(home_bp, name = "home")
    app.register_blueprint(matriculas_bp, name = "matriculas")
    app.register_blueprint(profesores_bp, name = "profesores")

    # Redireccionamiento
    @app.route("/")
    def index():
        return redirect(url_for('home.home'))
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(
        host = SERVER_IP,               
        port = SERVER_PORT,           
        debug= True
    )