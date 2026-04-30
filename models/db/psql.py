from .decorators import with_cursor, with_transactions
from .querys import (
    SELECT_VERSION, CREATE_ALUMNOS, CREATE_CURSOS, CREATE_MATRICULAS, CREATE_PROFESORES
)
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


if __name__ == "__main__":
    pg = PostgreSQL()
    result = pg.obtain_database_version()
    print(result) 

