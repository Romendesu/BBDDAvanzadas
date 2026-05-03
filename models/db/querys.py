# Operaciones de la Base de Datos (CRUD)

"""
OPERACIONES CREATE: 
    En este apartado nos encontraremos con las operaciones que involucren la creación de nuevos 
    registros o entidades dentro de la base de datos.

    Consultas disponibles:
        1. Creación de tablas dentro de la base de datos
        2. Creación de indices para la base de datos
        3. Ingresar elementos dentro de la base de datos
"""


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

# Generación de Indices
CREATE_INDEX_CURSOS_PROFESOR_ID = """
    CREATE INDEX idx_cursos_profesor_id ON cursos (profesor_id);
"""

CREATE_INDEX_MATRICULAS_CURSO_ID = """
    CREATE INDEX idx_matriculas_curso_id ON matriculas (curso_id);
"""

CREATE_INDEX_ALUMNOS_EMAIL = """      
    CREATE INDEX idx_alumnos_email ON alumnos (email);
"""

# Ingresar elementos dentro de la BB.DD
INSERT_ALUMNOS = """
    INSERT INTO alumnos (id, nombre, email) 
    VALUES (%s, %s, %s)
"""

INSERT_PROFESORES = """
    INSERT INTO profesores (id, nombre) 
    VALUES (%s, %s)
"""

INSERT_CURSOS = """
    INSERT INTO cursos (id, nombre, profesor_id) 
    VALUES (%s, %s, %s)
"""

INSERT_MATRICULAS = """
    INSERT INTO matriculas (alumno_id, curso_id, created_at) 
    VALUES (%s, %s, %s)
"""

"""
    OPERACIONES CREATE: 
        En este apartado nos encontraremos con las operaciones que involucren la lectura o la 
        consulta de registros de datos existentes dentro de una base de datos.

        Operaciones disponibles:
            1. Consultar información dentro de la propia base de datos
            2. Contar cuantas instancias existen dentro de una determinada tabla

"""
# Seleccionar la version de la base de datos
SELECT_VERSION = "SELECT version();"

# Contar el numero de elementos de una base de datos
COUNT_PROFESORES = "SELECT COUNT(*) FROM profesores;"
COUNT_ALUMNOS = "SELECT COUNT(*) FROM alumnos;"
COUNT_CURSOS = "SELECT COUNT(*) FROM cursos;"
COUNT_MATRICULAS = "SELECT COUNT(*) FROM matriculas;"

# Seleccionar todos los profesores y alumnos disponibles
SELECT_ALL_PROFESORES = """
    SELECT id, nombre FROM profesores;
"""
SELECT_ALL_ALUMNOS = """
    SELECT id, nombre, email FROM estudiantes;
"""
# Seleccionar varios profesor y alumnos dado su nombre
SELECT_PROFESORES_BY_NAME = """
    SELECT id, nombre FROM profesores WHERE nombre = %s;
"""
SELECT_ALUMNOS_BY_NAME = """
    SELECT id, nombre, email FROM alumnos WHERE nombre = %s;
"""

# Seleccionar un alumno y profesor dados su id
SELECT_PROFESORES_BY_ID = """
    SELECT id, nombre FROM profesores WHERE id = %s;
"""
SELECT_ALUMNOS_BY_NAME = """
    SELECT id, nombre, email FROM alumnos WHERE id = %s;
"""

"""
    Operaciones UPDATE:
        En este apartado, nos encontramos con las operaciones que involucran la modificación o 
        actualización de datos existentes dentro de la base de datos.

        Operaciones disponibles:
            Ninguna por el momento
"""

"""
    Operaciones DELETE:
        En este apartado, nos encontramos con las operaciones que involucran la eliminación de 
        registros o entidades existentes dentro de la base de datos.

        Operaciones disponibles:
            Ninguna por el momento
"""
