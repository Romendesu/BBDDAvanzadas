from .decorators import with_cursor

class PostgreSQL():
    # Obtener la version de PostgreSQL
    @with_cursor
    def obtain_database_version(self, cursor, query:str = "SELECT version();"):
        cursor.execute(query)
        return cursor.fetchone()


if __name__ == "__main__":
    pg = PostgreSQL()
    result = pg.obtain_database_version()
    print(result) 

