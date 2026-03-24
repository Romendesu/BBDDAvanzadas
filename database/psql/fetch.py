from __future__ import annotations
import psycopg
from psql.config import load_config
from psql.querys import SELECT_TEACHERS, SELECT_STUDENTS, SELECT_GRADES
from database.models.entities import Profesor, Alumno, Curso

# Obtener todos los profesores
def get_teachers() -> list[Profesor]:
    cfg = load_config()
    teachers_list = []

    with psycopg.connect(**cfg) as conn:
        with conn.cursor() as cur:
            cur.execute(SELECT_TEACHERS)
            rows = cur.fetchall()
            # Convertimos cada tupla en un objeto 
            for row in rows:
                teacher_obj = Profesor(*row) 
                teachers_list.append(teacher_obj)

    return teachers_list

# Obtener todos los estudiantes
def get_students() -> list[Alumno]:
    cfg = load_config()
    students_list = []

    with psycopg.connect(**cfg) as conn:
        with conn.cursor() as cur:
            cur.execute(SELECT_STUDENTS)
            rows = cur.fetchall()
            # Convertimos cada tupla en un objeto 
            for row in rows:
                students_obj = Alumno(*row) 
                students_list.append(students_obj)

    return students_list

# Obtener todos los cursos
def get_grades() -> list[Curso]:
    cfg = load_config()
    grades_list = []

    with psycopg.connect(**cfg) as conn:
        with conn.cursor() as cur:
            cur.execute(SELECT_GRADES)
            rows = cur.fetchall()
            # Convertimos cada tupla en un objeto 
            for row in rows:
                grades_obj = Curso(*row) 
                grades_list.append(grades_obj)

    return grades_list