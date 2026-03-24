from __future__ import annotations

import psycopg
from psycopg import OperationalError
from .config import load_config
from .querys import COUNT_ALUMNOS, COUNT_CURSOS, COUNT_MATRICULAS, COUNT_PROFESORES

def count_elements():
    cfg = load_config()
    # Importante: El orden en la lista 'querys' debe coincidir con el orden en que
    # procesaremos las claves si lo haces por índice, o mejor, usa un mapeo:
    
    queries_map = {
        "alumnos": COUNT_ALUMNOS,
        "cursos": COUNT_CURSOS,
        "matriculas": COUNT_MATRICULAS,
        "profesores": COUNT_PROFESORES
    }
    
    counted_dict = {
        "alumnos": 0,
        "profesores": 0,
        "cursos": 0,
        "matriculas": 0
    }
    
    try:
        with psycopg.connect(**cfg) as conn:
            with conn.cursor() as cur:
                for key, query in queries_map.items():
                    cur.execute(query)
                    record = cur.fetchone()
                    if record:
                        counted_dict[key] = record[0]
        
        # El return debe estar FUERA del bucle para devolver el diccionario completo
        return counted_dict

    except OperationalError as e:
        print("Error de conexión:", e)
        return counted_dict # Devolvemos el dict con ceros en caso de fallo
