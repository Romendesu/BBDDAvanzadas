from __future__ import annotations
import psycopg
from database.psql.config import load_config
from database.psql.querys import COPY_ALUMNOS, COPY_CURSOS, COPY_MATRICULAS, COPY_PROFESORES
import os

def load_profesores_from_csv(file_path: str) -> None:
    """Carga masiva de profesores desde CSV."""
    cfg = load_config()
    with psycopg.connect(**cfg) as conn:
        with conn.cursor() as cur:
            with open(file_path, 'r', encoding='utf-8') as f:
                with cur.copy(COPY_PROFESORES) as copy:
                    while data := f.read(8192):
                        copy.write(data)
    print(f"Profesores cargados desde {file_path}")

def load_alumnos_from_csv(file_path: str) -> None:
    """Carga masiva de alumnos desde CSV."""
    cfg = load_config()
    with psycopg.connect(**cfg) as conn:
        with conn.cursor() as cur:
            with open(file_path, 'r', encoding='utf-8') as f:
                with cur.copy(COPY_ALUMNOS) as copy:
                    while data := f.read(8192):
                        copy.write(data)
    print(f"Alumnos cargados desde {file_path}")

def load_cursos_from_csv(file_path: str) -> None:
    """Carga masiva de cursos desde CSV."""
    cfg = load_config()
    with psycopg.connect(**cfg) as conn:
        with conn.cursor() as cur:
            with open(file_path, 'r', encoding='utf-8') as f:
                with cur.copy(COPY_CURSOS) as copy:
                    while data := f.read(8192):
                        copy.write(data)
    print(f"Cursos cargados desde {file_path}")

def load_matriculas_from_csv(file_path: str) -> None:
    """Carga masiva de matrículas desde CSV. Vital para los 7.5M de filas."""
    cfg = load_config()
    with psycopg.connect(**cfg) as conn:
        with conn.cursor() as cur:
            with open(file_path, 'r', encoding='utf-8') as f:
                # Usamos el comando COPY de PostgreSQL a través de psycopg
                with cur.copy(COPY_MATRICULAS) as copy:
                    while data := f.read(8192):
                        copy.write(data)
    print(f"Matrículas cargadas desde {file_path}")

def insert():
    from utils import FAKE_INFO_URL as FOLDER   
    import time
    start = time.time()
    load_profesores_from_csv(os.path.join(FOLDER, "profesores.csv"))
    load_alumnos_from_csv(os.path.join(FOLDER, "alumnos.csv"))
    load_cursos_from_csv(os.path.join(FOLDER, "cursos.csv"))
    load_matriculas_from_csv(os.path.join(FOLDER, "matriculas.csv"))
    end = time.time()
    total = end - start
    print("¡Carga masiva completada exitosamente!")
    print(f"La operación tardó: {total:.4f} segundos")

if __name__ == "__main__":
    insert()