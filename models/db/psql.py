from .decorators import with_cursor, with_transactions
from .querys import (
    SELECT_VERSION, SELECT_ALL_PROFESORES, SELECT_ALL_ALUMNOS,
    COUNT_PROFESORES, COUNT_ALUMNOS, COUNT_CURSOS, COUNT_MATRICULAS,
    CREATE_ALUMNOS, CREATE_CURSOS, CREATE_MATRICULAS, CREATE_PROFESORES,
    INSERT_ALUMNOS, INSERT_PROFESORES
)
from ..entities import Alumnos, Profesores
from psycopg2 import Error
# Funciones auxiliares
def validate_email(email: str) -> bool:
    import re
    REGEX_PATTERN = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}" 
    if re.match(REGEX_PATTERN, email):
        return True   
    return False

# Operaciones principales de PostgreSQL
class PostgreSQL():
    # Obtener la version de PostgreSQL
    @with_cursor
    def obtain_database_version(self, cursor):
        cursor.execute(SELECT_VERSION)
        return cursor.fetchone()

    # Creacion de todas las tablas de Postgresql
    @with_transactions
    def create_tables(self, cursor):
        cursor.execute(CREATE_ALUMNOS)
        cursor.execute(CREATE_PROFESORES)
        cursor.execute(CREATE_CURSOS)
        cursor.execute(CREATE_MATRICULAS)

# Operaciones del profesor
class OperacionesProfesor():
    # Operaciones de lectura   
    @with_cursor
    def get_count(self, cursor):
        cursor.execute(COUNT_PROFESORES)
        result = cursor.fetchone()
        return result[0] if result else 0
    
    @with_cursor
    def get_all_teachers(self, cursor):
        try:
            cursor.execute(SELECT_ALL_PROFESORES)
            return cursor.fetchall()
        except (Exception, Error) as e:
            print("Error al obtener los profesores:", e)
            return []

    
    # Operaciones de escritura   
    @with_transactions
    def insert_one_teacher(self, cursor, profesor:Profesores):
        params = (profesor.id, profesor.nombre)
        cursor.execute(INSERT_PROFESORES, params)
        print(f"Se ha ingresado el profesor: {profesor} dentro de la base de datos")

# Operaciones del Alumno
class OperacionesAlumno():   
    # Operaciones de lectura   
    @with_cursor
    def get_count(self, cursor):
        cursor.execute(COUNT_ALUMNOS)
        result = cursor.fetchone()
        return result[0] if result else 0
    
    @with_cursor
    def get_all_students(self, cursor):
        try:
            cursor.execute(SELECT_ALL_ALUMNOS)
            return cursor.fetchall()
        except (Exception, Error) as e:
            print("Error al obtener los estudiantes:", e)
            return []


    # Operaciones de escritura   
    @with_transactions
    def insert_one_student(self, cursor, alumno:Alumnos):
        # Verificamos el formato del correo
        if not alumno.email or not validate_email(alumno.email):
            raise Exception("Hay un error procesando el correo electrónico.")

        params = (alumno.id, alumno.nombre, alumno.email)
        cursor.execute(INSERT_ALUMNOS, params)
        print(f"Se ha ingresado el alumno: {alumno} dentro de la base de datos")

# Operaciones del Curso
class OperacionesCurso():   
    @with_cursor
    def get_count(self, cursor):
        cursor.execute(COUNT_CURSOS)
        result = cursor.fetchone()
        return result[0] if result else 0
# Operaciones de la matricula
class OperacionesMatricula():   
    @with_cursor
    def get_count(self, cursor):
        cursor.execute(COUNT_MATRICULAS)
        result = cursor.fetchone()
        return result[0] if result else 0
    

