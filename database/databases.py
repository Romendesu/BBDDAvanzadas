# Archivo que contendrá todas las operaciones encapsuladas en una clase
import sys
import os
sys.path.append(os.path.dirname(__file__))

from psql import insert, connect, create_tables, get_database_statistics

class PostgreSQL:
    def __init__(self) -> None:
        pass
    
    # Conexion con la base de datos
    def connect_db(self):
        return connect()
    
    # Crear tablas
    def create_tables_db(self):
        return create_tables()
    
    # Ingresar valores (dentro de un .csv)
    def insert_db(self):
        return insert()
    
    # Conteo de elementos
    def get_stats(self):
        return get_database_statistics()
    
    
if __name__ == "__main__":
    # Inicio
    db = PostgreSQL()
    db.connect_db()
    db.create_tables_db()
    add_items = int(input("Desea meter elementos? 1: SI, 2: NO"))
    if (add_items == 1):
        db.insert_db()
    db.get_stats()
    
