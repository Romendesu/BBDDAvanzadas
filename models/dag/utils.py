import psycopg2
from config import PG_HOST, PG_NAME, PG_USER, PG_PASSWORD, PG_PORT, SQLITE_PATH

# Conexión a PostgreSQL

PG_CONN = {
    "host":     PG_HOST,
    "database": PG_NAME,
    "user":     PG_USER,
    "password": PG_PASSWORD,
    "port":     PG_PORT,
}


def get_pg_conn():
    return psycopg2.connect(**PG_CONN)


def already_seeded(cur, table: str, min_rows: int) -> bool:
    cur.execute(f"SELECT COUNT(*) FROM {table};")
    return cur.fetchone()[0] >= min_rows


# Dataset mínimo PostgreSQL

PROFESORES_NOMBRES = [
    "Ana García López",      "Carlos Martínez Ruiz",  "Elena Sánchez Pérez",
    "Fernando Torres Alba",  "Isabel Romero Díaz",     "Javier Moreno Castro",
    "Laura Jiménez Vega",    "Miguel Hernández Gil",   "Natalia Flores Reyes",
    "Pablo Navarro Serrano",
]

CURSOS_NOMBRES = [
    "Álgebra Lineal",                    "Cálculo Diferencial",
    "Bases de Datos Avanzadas",          "Estructuras de Datos",
    "Sistemas Operativos",               "Redes de Computadores",
    "Inteligencia Artificial",           "Programación Funcional",
    "Arquitectura de Software",          "Seguridad Informática",
    "Computación en la Nube",            "Machine Learning",
    "Diseño de Interfaces",              "Ingeniería de Software",
    "Matemáticas Discretas",             "Compiladores",
    "Visión por Computador",             "Criptografía",
    "Procesamiento de Lenguaje Natural", "Robótica",
]

# Usuarios SQLite

USUARIOS = [
    {
        "username":  "admin",
        "email":     "admin@academico.es",
        "password":  "Admin1234!",
        "nombre":    "Administrador del Sistema",
        "rol":       "admin",
        "is_active": 1,
    },
    {
        "username":  "profesor",
        "email":     "profesor@academico.es",
        "password":  "Profesor1234!",
        "nombre":    "Profesor Demo",
        "rol":       "profesor",
        "is_active": 1,
    },
    {
        "username":  "alumno",
        "email":     "alumno@academico.es",
        "password":  "Alumno1234!",
        "nombre":    "Alumno Demo",
        "rol":       "alumno",
        "is_active": 1,
    },
]
