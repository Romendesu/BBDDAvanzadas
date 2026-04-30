# Operaciones de la Base de Datos (CRUD)
# CREATE
CREATE_ALUMNOS = """
    CREATE TABLE IF NOT EXISTS alumnos (
        id UUID PRIMARY KEY, 
        nombre VARCHAR(100) NOT NULL,
        email VARCHAR(100) NOT NULL
    );
"""

CREATE_PROFESORES = """
    CREATE TABLE IF NOT EXISTS profesores (
        id UUID PRIMARY KEY,
        nombre VARCHAR(100) NOT NULL
    );
"""

CREATE_CURSOS = """
    CREATE TABLE IF NOT EXISTS cursos (
        id UUID PRIMARY KEY,
        nombre VARCHAR(100) NOT NULL,
        profesor_id UUID NOT NULL,
        FOREIGN KEY (profesor_id) REFERENCES profesores(id)
            ON DELETE RESTRICT
            ON UPDATE CASCADE
    );
"""

CREATE_MATRICULAS = """
    CREATE TABLE IF NOT EXISTS matriculas (
        alumno_id UUID NOT NULL,
        curso_id UUID NOT NULL,
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        PRIMARY KEY (alumno_id, curso_id),
        FOREIGN KEY (alumno_id) REFERENCES alumnos(id) ON DELETE CASCADE,
        FOREIGN KEY (curso_id)  REFERENCES cursos(id)  ON DELETE CASCADE
    );
"""
# READ
SELECT_VERSION = "SELECT version();"
COUNT_PROFESORES = "SELECT COUNT(*) FROM profesores;"
COUNT_ALUMNOS = "SELECT COUNT(*) FROM alumnos;"
COUNT_CURSOS = "SELECT COUNT(*) FROM cursos;"
COUNT_MATRICULAS = "SELECT COUNT(*) FROM matriculas;"

# UPDATE
# DELETE
