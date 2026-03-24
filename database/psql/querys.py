import os
DDL = (
    # 1. Tabla de Profesores
    '''
    CREATE TABLE IF NOT EXISTS profesor (
        id_profesor SERIAL PRIMARY KEY,
        nombre VARCHAR(150) NOT NULL,
        correo VARCHAR(150),
        especialidad VARCHAR(150),
        fecha_contratacion DATE DEFAULT CURRENT_DATE
    );
    ''',
    
    # 2. Tabla de Alumnos
    '''
    CREATE TABLE IF NOT EXISTS alumno (
        id_alumno SERIAL PRIMARY KEY,
        nombre VARCHAR(150) NOT NULL,
        correo VARCHAR(150),
        fecha_nacimiento DATE
    );
    ''',
    
    # 3. Tabla de Cursos (Depende de Profesor)
    '''
    CREATE TABLE IF NOT EXISTS curso (
        id_curso SERIAL PRIMARY KEY,
        nombre_curso VARCHAR(200) NOT NULL,
        id_profesor INTEGER,
        FOREIGN KEY (id_profesor)
            REFERENCES profesor (id_profesor)
            ON UPDATE CASCADE
            ON DELETE SET NULL
    );
    ''',
    
    # 4. Tabla de Matrículas (Relación N:M entre Alumno y Curso)
    '''
    CREATE TABLE IF NOT EXISTS matricula (
        id_curso INTEGER NOT NULL,
        id_alumno INTEGER NOT NULL,
        fecha_inscripcion DATE DEFAULT '2026-02-01',
        nota_final DECIMAL(4,2),
        PRIMARY KEY (id_curso, id_alumno),
        FOREIGN KEY (id_curso)
            REFERENCES curso (id_curso)
            ON UPDATE CASCADE
            ON DELETE CASCADE,
        FOREIGN KEY (id_alumno)
            REFERENCES alumno (id_alumno)
            ON UPDATE CASCADE
            ON DELETE CASCADE
    );
    '''
)
# Consultas de Carga Masiva (COPY)

COPY_PROFESORES = """
    COPY profesor (id_profesor, nombre, correo, especialidad, fecha_contratacion) 
    FROM STDIN 
    WITH (FORMAT CSV, DELIMITER ',');
"""

COPY_ALUMNOS = """
    COPY alumno (id_alumno, nombre, correo, fecha_nacimiento) 
    FROM STDIN 
    WITH (FORMAT CSV, DELIMITER ',');
"""

COPY_CURSOS = """
    COPY curso (id_curso, nombre_curso, id_profesor) 
    FROM STDIN 
    WITH (FORMAT CSV, DELIMITER ',');
"""

COPY_MATRICULAS = """
    COPY matricula (id_curso, id_alumno, fecha_inscripcion, nota_final) 
    FROM STDIN 
    WITH (FORMAT CSV, DELIMITER ',');
"""

COUNT_PROFESORES = """
    SELECT COUNT(*) FROM profesor;
"""

COUNT_ALUMNOS = """
    SELECT COUNT(*) FROM alumno;
"""

COUNT_CURSOS = """
    SELECT COUNT(*) FROM curso;
"""

COUNT_MATRICULAS = """
    SELECT COUNT(*) FROM matricula;
"""

SELECT_TEACHERS = """
    SELECT id_profesor, nombre, especialidad, correo, fecha_contratacion FROM profesor;
"""

SELECT_STUDENTS = """
    SELECT id_alumno, nombre, correo, fecha_nacimiento FROM alumno;
"""

SELECT_GRADES = """
    SELECT id_curso, nombre_curso, id_profesor FROM curso;
"""