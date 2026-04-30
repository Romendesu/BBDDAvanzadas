from .decorators import with_cursor, with_transactions
from .querys import (
    SELECT_VERSION, COUNT_PROFESORES, COUNT_ALUMNOS, COUNT_CURSOS, COUNT_MATRICULAS,
    CREATE_ALUMNOS, CREATE_CURSOS, CREATE_MATRICULAS, CREATE_PROFESORES,
)

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
    @with_cursor
    def get_count(self, cursor):
        cursor.execute(COUNT_PROFESORES)
        return cursor.fetchone()

# Operaciones del Alumno
class OperacionesAlumno():   
    @with_cursor
    def get_count(self, cursor):
        cursor.execute(COUNT_ALUMNOS)
        return cursor.fetchone()
   
# Operaciones del Curso
class OperacionesCurso():   
    @with_cursor
    def get_count(self, cursor):
        cursor.execute(COUNT_CURSOS)
        return cursor.fetchone()
# Operaciones de la matricula
class OperacionesMatricula():   
    @with_cursor
    def get_count(self, cursor):
        cursor.execute(COUNT_MATRICULAS)
        return cursor.fetchone()
    

