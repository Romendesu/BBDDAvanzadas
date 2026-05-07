"""
OPERACIONES SQLITE:
    Consultas sobre la base de datos de autenticación (auth.db).
"""

SELECT_USUARIO_BY_USERNAME = """
    SELECT * FROM usuarios WHERE username = ? AND is_active = 1;
"""

SELECT_USUARIO_EXISTS = """
    SELECT id FROM usuarios WHERE username = ?;
"""

CREATE_SQLITE_USUARIOS = """
    CREATE TABLE IF NOT EXISTS usuarios (
        id            INTEGER PRIMARY KEY AUTOINCREMENT,
        username      TEXT    NOT NULL UNIQUE,
        email         TEXT    NOT NULL UNIQUE,
        password_hash TEXT    NOT NULL,
        nombre        TEXT    NOT NULL,
        rol           TEXT    NOT NULL DEFAULT 'alumno'
                              CHECK (rol IN ('admin', 'profesor', 'alumno')),
        is_active     INTEGER NOT NULL DEFAULT 1,
        created_at    TEXT    NOT NULL
    );
"""

CREATE_SQLITE_INDEX_USERNAME = """
    CREATE UNIQUE INDEX IF NOT EXISTS idx_usuarios_username ON usuarios (username);
"""

CREATE_SQLITE_INDEX_EMAIL = """
    CREATE UNIQUE INDEX IF NOT EXISTS idx_usuarios_email ON usuarios (email);
"""

INSERT_USUARIO = """
    INSERT INTO usuarios (username, email, password_hash, nombre, rol, is_active, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?);
"""

"""
OPERACIONES CREATE:
    Consultas para la creación de tablas, índices e inserción de nuevos registros.
"""

CREATE_ALUMNOS = """
    CREATE TABLE IF NOT EXISTS alumnos (
        id UUID PRIMARY KEY,
        nombre VARCHAR(100) NOT NULL,
        email VARCHAR(100) NOT NULL
    );
"""

# Migrations: add new columns if not present
ALTER_ALUMNOS_SALDO = """
    ALTER TABLE alumnos ADD COLUMN IF NOT EXISTS saldo NUMERIC(10,2) NOT NULL DEFAULT 500.00;
"""
ALTER_CURSOS_PRECIO = """
    ALTER TABLE cursos ADD COLUMN IF NOT EXISTS precio NUMERIC(10,2) NOT NULL DEFAULT 100.00;
"""
ALTER_CURSOS_MAX_ALUMNOS = """
    ALTER TABLE cursos ADD COLUMN IF NOT EXISTS max_alumnos INTEGER NOT NULL DEFAULT 30;
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


CREATE_INDEX_CURSOS_PROFESOR_ID = """
    CREATE INDEX IF NOT EXISTS idx_cursos_profesor_id ON cursos (profesor_id);
"""

CREATE_INDEX_MATRICULAS_CURSO_ID = """
    CREATE INDEX IF NOT EXISTS idx_matriculas_curso_id ON matriculas (curso_id);
"""

CREATE_INDEX_ALUMNOS_EMAIL = """
    CREATE INDEX IF NOT EXISTS idx_alumnos_email ON alumnos (email);
"""

# Índices para acelerar las búsquedas por filtro
CREATE_INDEX_ALUMNOS_NOMBRE     = "CREATE INDEX IF NOT EXISTS idx_alumnos_nombre      ON alumnos (nombre);"
CREATE_INDEX_ALUMNOS_SALDO      = "CREATE INDEX IF NOT EXISTS idx_alumnos_saldo       ON alumnos (saldo);"
CREATE_INDEX_CURSOS_NOMBRE      = "CREATE INDEX IF NOT EXISTS idx_cursos_nombre       ON cursos  (nombre);"
CREATE_INDEX_CURSOS_PRECIO      = "CREATE INDEX IF NOT EXISTS idx_cursos_precio       ON cursos  (precio);"
CREATE_INDEX_CURSOS_MAX_ALUMNOS = "CREATE INDEX IF NOT EXISTS idx_cursos_max_alumnos  ON cursos  (max_alumnos);"
CREATE_INDEX_PROFESORES_NOMBRE  = "CREATE INDEX IF NOT EXISTS idx_profesores_nombre   ON profesores (nombre);"
CREATE_INDEX_MATRICULAS_DATE    = "CREATE INDEX IF NOT EXISTS idx_matriculas_date     ON matriculas (created_at);"
CREATE_INDEX_AUDITORIA_DATE     = "CREATE INDEX IF NOT EXISTS idx_auditoria_date      ON auditoria (created_at);"
CREATE_INDEX_AUDITORIA_ACCION   = "CREATE INDEX IF NOT EXISTS idx_auditoria_accion    ON auditoria (accion);"
CREATE_INDEX_AUDITORIA_USUARIO  = "CREATE INDEX IF NOT EXISTS idx_auditoria_usuario   ON auditoria (usuario);"


INSERT_ALUMNOS = """
    INSERT INTO alumnos (id, nombre, email, saldo)
    VALUES (%s, %s, %s, %s)
"""

INSERT_PROFESORES = """
    INSERT INTO profesores (id, nombre)
    VALUES (%s, %s)
"""

INSERT_CURSOS = """
    INSERT INTO cursos (id, nombre, profesor_id, precio, max_alumnos)
    VALUES (%s, %s, %s, %s, %s)
"""

INSERT_MATRICULAS = """
    INSERT INTO matriculas (alumno_id, curso_id, created_at)
    VALUES (%s, %s, %s)
"""


"""
OPERACIONES READ:
    Consultas para la lectura y consulta de registros existentes en la base de datos.
"""

SELECT_VERSION = "SELECT version();"

COUNT_PROFESORES = "SELECT COUNT(*) FROM profesores;"
COUNT_ALUMNOS    = "SELECT COUNT(*) FROM alumnos;"
COUNT_CURSOS     = "SELECT COUNT(*) FROM cursos;"
COUNT_MATRICULAS = "SELECT COUNT(*) FROM matriculas;"

SELECT_ALL_PROFESORES = """
    SELECT id, nombre FROM profesores;
"""
SELECT_ALL_ALUMNOS = """
    SELECT id, nombre, email, saldo FROM alumnos;
"""
SELECT_ALL_CURSOS = """
    SELECT c.id, c.nombre, p.nombre AS profesor, c.precio, c.max_alumnos FROM cursos c
    JOIN profesores p ON c.profesor_id = p.id;
"""
SELECT_ALL_MATRICULAS = """
    SELECT a.nombre AS alumno, c.nombre AS curso, m.created_at
    FROM matriculas m
    JOIN alumnos a ON m.alumno_id = a.id
    JOIN cursos c ON m.curso_id = c.id
    ORDER BY m.created_at DESC;
"""

# Consultas enriquecidas para las vistas de tabla
SELECT_ALUMNOS_WITH_COUNT = """
    SELECT a.id, a.nombre, a.email, a.saldo, COUNT(m.curso_id) AS n_matriculas
    FROM alumnos a
    LEFT JOIN matriculas m ON a.id = m.alumno_id
    GROUP BY a.id, a.nombre, a.email, a.saldo
    ORDER BY a.nombre;
"""
SELECT_PROFESORES_WITH_COUNT = """
    SELECT p.id, p.nombre,
           COUNT(DISTINCT c.id)       AS n_cursos,
           COUNT(DISTINCT m.alumno_id) AS n_alumnos
    FROM profesores p
    LEFT JOIN cursos c     ON c.profesor_id = p.id
    LEFT JOIN matriculas m ON m.curso_id = c.id
    GROUP BY p.id, p.nombre
    ORDER BY p.nombre;
"""
SELECT_CURSOS_WITH_COUNT = """
    SELECT c.id, c.nombre, p.nombre AS profesor, COUNT(m.alumno_id) AS n_alumnos,
           c.precio, c.max_alumnos
    FROM cursos c
    JOIN  profesores p  ON c.profesor_id = p.id
    LEFT JOIN matriculas m ON m.curso_id = c.id
    GROUP BY c.id, c.nombre, p.nombre, c.precio, c.max_alumnos
    ORDER BY c.nombre;
"""
SELECT_MATRICULAS_FULL = """
    SELECT a.nombre AS alumno, c.nombre AS curso, p.nombre AS profesor, m.created_at,
           m.alumno_id, m.curso_id
    FROM matriculas m
    JOIN alumnos a    ON m.alumno_id  = a.id
    JOIN cursos c     ON m.curso_id   = c.id
    JOIN profesores p ON c.profesor_id = p.id
    ORDER BY m.created_at DESC;
"""

# Consultas de detalle por ID
SELECT_PROFESOR_BY_ID = """
    SELECT p.id, p.nombre,
           COUNT(DISTINCT c.id)        AS n_cursos,
           COUNT(DISTINCT m.alumno_id) AS n_alumnos
    FROM profesores p
    LEFT JOIN cursos c     ON c.profesor_id = p.id
    LEFT JOIN matriculas m ON m.curso_id = c.id
    WHERE p.id = %s
    GROUP BY p.id, p.nombre;
"""
SELECT_CURSOS_BY_PROFESOR = """
    SELECT c.id, c.nombre, COUNT(m.alumno_id) AS n_alumnos
    FROM cursos c
    LEFT JOIN matriculas m ON m.curso_id = c.id
    WHERE c.profesor_id = %s
    GROUP BY c.id, c.nombre
    ORDER BY c.nombre;
"""
SELECT_ALUMNO_BY_ID = """
    SELECT a.id, a.nombre, a.email,
           COUNT(m.curso_id) AS n_matriculas,
           a.saldo
    FROM alumnos a
    LEFT JOIN matriculas m ON m.alumno_id = a.id
    WHERE a.id = %s
    GROUP BY a.id, a.nombre, a.email, a.saldo;
"""
SELECT_CURSOS_BY_ALUMNO = """
    SELECT c.id, c.nombre, p.nombre AS profesor, m.created_at
    FROM matriculas m
    JOIN cursos c     ON m.curso_id    = c.id
    JOIN profesores p ON c.profesor_id = p.id
    WHERE m.alumno_id = %s
    ORDER BY m.created_at DESC;
"""
SELECT_CURSO_BY_ID = """
    SELECT c.id, c.nombre, p.id AS profesor_id, p.nombre AS profesor,
           COUNT(m.alumno_id) AS n_alumnos, c.precio, c.max_alumnos
    FROM cursos c
    JOIN profesores p  ON c.profesor_id = p.id
    LEFT JOIN matriculas m ON m.curso_id = c.id
    WHERE c.id = %s
    GROUP BY c.id, c.nombre, p.id, p.nombre, c.precio, c.max_alumnos;
"""
SELECT_ALUMNOS_BY_CURSO = """
    SELECT a.id, a.nombre, a.email, m.created_at
    FROM matriculas m
    JOIN alumnos a ON m.alumno_id = a.id
    WHERE m.curso_id = %s
    ORDER BY m.created_at DESC;
"""
CHECK_MATRICULA_EXISTS = """
    SELECT 1 FROM matriculas WHERE alumno_id = %s AND curso_id = %s;
"""

SELECT_PROFESORES_BY_NAME = """
    SELECT id, nombre FROM profesores WHERE nombre = %s;
"""
SELECT_ALUMNOS_BY_ID = """
    SELECT id, nombre, email FROM alumnos WHERE id = %s;
"""


"""
TABLA DE AUDITORÍA:
    Registro de todas las operaciones CREATE/UPDATE/DELETE sobre las entidades principales.
"""

CREATE_AUDITORIA = """
    CREATE TABLE IF NOT EXISTS auditoria (
        id          SERIAL PRIMARY KEY,
        usuario     VARCHAR(100) NOT NULL,
        accion      VARCHAR(20)  NOT NULL CHECK (accion IN ('CREATE', 'UPDATE', 'DELETE')),
        entidad     VARCHAR(50)  NOT NULL,
        entidad_id  VARCHAR(100),
        detalle     TEXT,
        created_at  TIMESTAMPTZ  NOT NULL DEFAULT NOW()
    );
"""

CREATE_INDEX_AUDITORIA_ENTIDAD = """
    CREATE INDEX IF NOT EXISTS idx_auditoria_entidad ON auditoria (entidad);
"""

INSERT_AUDITORIA = """
    INSERT INTO auditoria (usuario, accion, entidad, entidad_id, detalle)
    VALUES (%s, %s, %s, %s, %s);
"""

SELECT_ALL_AUDITORIA = """
    SELECT id, usuario, accion, entidad, entidad_id, detalle, created_at
    FROM auditoria
    ORDER BY created_at DESC;
"""

COUNT_AUDITORIA = "SELECT COUNT(*) FROM auditoria;"

DELETE_AUDITORIA = "DELETE FROM auditoria WHERE id = %s;"

DELETE_ALL_AUDITORIA = "DELETE FROM auditoria;"

"""
OPERACIONES UPDATE:
    Consultas para la modificación o actualización de registros existentes.

    Operaciones disponibles: ninguna por el momento.
"""


"""
OPERACIONES DELETE:
    Consultas para la eliminación de registros existentes en la base de datos.
"""

DELETE_PROFESOR  = "DELETE FROM profesores WHERE id = %s;"
DELETE_ALUMNO    = "DELETE FROM alumnos   WHERE id = %s;"
DELETE_CURSO     = "DELETE FROM cursos    WHERE id = %s;"
DELETE_MATRICULA = "DELETE FROM matriculas WHERE alumno_id = %s AND curso_id = %s;"

"""
DEMOS DE TRANSACCIONES:
    Consultas auxiliares usadas en las demos de la página de Transacciones.
"""

DEMO_SELECT_ALUMNO_LIMIT1    = "SELECT id FROM alumnos LIMIT 1;"
DEMO_SELECT_MATRICULA_LIMIT1 = "SELECT alumno_id, curso_id FROM matriculas LIMIT 1;"
DEMO_INSERT_MATRICULA_RAW    = "INSERT INTO matriculas (alumno_id, curso_id, created_at) VALUES (%s, %s, NOW());"
DEMO_COUNT_MATRICULAS_CURSO  = "SELECT COUNT(*) FROM matriculas WHERE curso_id = %s;"
DEMO_INSERT_ALUMNO_TEMP      = "INSERT INTO alumnos (id, nombre, email, saldo) VALUES (%s, %s, %s, %s);"
DEMO_SELECT_ALUMNO_BY_ID     = "SELECT id, nombre FROM alumnos WHERE id = %s;"
DEMO_DELETE_ALUMNO_BY_ID     = "DELETE FROM alumnos WHERE id = %s;"

"""
MATRICULACIÓN TRANSACCIONAL:
    Consultas para el proceso de matriculación con control explícito de transacción.
"""

SELECT_ALUMNO_FOR_ENROLL = """
    SELECT id, nombre, saldo FROM alumnos WHERE id = %s FOR UPDATE;
"""

SELECT_CURSO_FOR_ENROLL = """
    SELECT c.id, c.nombre, c.precio, c.max_alumnos,
           (SELECT COUNT(*) FROM matriculas WHERE curso_id = c.id) AS n_inscritos
    FROM cursos c
    WHERE c.id = %s
    FOR UPDATE;
"""

UPDATE_ALUMNO_SALDO = """
    UPDATE alumnos SET saldo = saldo + %s WHERE id = %s;
"""

UPDATE_CURSO_SETTINGS = """
    UPDATE cursos SET precio = %s, max_alumnos = %s WHERE id = %s;
"""

UPDATE_ALUMNO_RECHARGE = """
    UPDATE alumnos SET saldo = saldo + %s WHERE id = %s;
"""

"""
VISTA: vista_matriculas_detalle
    Muestra alumno, profesor y asignatura de cada matrícula activa.
"""

CREATE_VISTA_MATRICULAS = """
    CREATE OR REPLACE VIEW vista_matriculas_detalle AS
    SELECT
        a.nombre  AS alumno,
        p.nombre  AS profesor,
        c.nombre  AS asignatura,
        m.created_at
    FROM matriculas m
    JOIN alumnos    a ON m.alumno_id   = a.id
    JOIN cursos     c ON m.curso_id    = c.id
    JOIN profesores p ON c.profesor_id = p.id;
"""

SELECT_VISTA_MATRICULAS = """
    SELECT alumno, profesor, asignatura, created_at
    FROM vista_matriculas_detalle
    ORDER BY created_at DESC;
"""

COUNT_VISTA_MATRICULAS = """
    SELECT COUNT(*) FROM vista_matriculas_detalle;
"""

"""
BASES PARA FILTROS DINÁMICOS (WHERE/HAVING + LIMIT/OFFSET ensamblado en Python)
    Cada BASE incluye SELECT+FROM+JOIN.
    Cada TAIL incluye GROUP BY+ORDER BY.
    El método Python añade WHERE, HAVING, LIMIT y OFFSET.
"""

# Alumnos  — filtros: nombre/email (ILIKE), saldo (>=, <=)
SELECT_ALUMNOS_FILTER_BASE = """
    SELECT a.id, a.nombre, a.email, a.saldo, COUNT(m.curso_id) AS n_matriculas
    FROM alumnos a
    LEFT JOIN matriculas m ON a.id = m.alumno_id
"""
SELECT_ALUMNOS_FILTER_TAIL = "    GROUP BY a.id, a.nombre, a.email, a.saldo ORDER BY a.nombre"

# Asignaturas — filtros: nombre (ILIKE), precio (>=,<=), max_alumnos (>=,<=)
SELECT_CURSOS_FILTER_BASE = """
    SELECT c.id, c.nombre, p.nombre AS profesor,
           COUNT(m.alumno_id) AS n_alumnos, c.precio, c.max_alumnos
    FROM cursos c
    JOIN  profesores p    ON c.profesor_id = p.id
    LEFT JOIN matriculas m ON m.curso_id = c.id
"""
SELECT_CURSOS_FILTER_TAIL = "    GROUP BY c.id, c.nombre, p.nombre, c.precio, c.max_alumnos ORDER BY c.nombre"

# Profesores — filtros: nombre (ILIKE), n_cursos (HAVING >=,<=)
SELECT_PROFESORES_FILTER_BASE = """
    SELECT p.id, p.nombre,
           COUNT(DISTINCT c.id)        AS n_cursos,
           COUNT(DISTINCT m.alumno_id) AS n_alumnos
    FROM profesores p
    LEFT JOIN cursos     c ON c.profesor_id = p.id
    LEFT JOIN matriculas m ON m.curso_id    = c.id
"""
SELECT_PROFESORES_FILTER_GROUP = "    GROUP BY p.id, p.nombre"
SELECT_PROFESORES_FILTER_ORDER = "    ORDER BY p.nombre"

# Matrículas — filtros: alumno/curso (ILIKE), fecha (>=,<=)
SELECT_MATRICULAS_FILTER_BASE = """
    SELECT a.nombre AS alumno, c.nombre AS curso, p.nombre AS profesor,
           m.created_at, m.alumno_id, m.curso_id
    FROM matriculas m
    JOIN alumnos    a ON m.alumno_id   = a.id
    JOIN cursos     c ON m.curso_id    = c.id
    JOIN profesores p ON c.profesor_id = p.id
"""
SELECT_MATRICULAS_FILTER_TAIL = "    ORDER BY m.created_at DESC"

# Vista — filtros: alumno/profesor/asignatura (ILIKE), fecha (>=,<=)
SELECT_VISTA_FILTER_BASE = "    SELECT alumno, profesor, asignatura, created_at FROM vista_matriculas_detalle"
SELECT_VISTA_FILTER_TAIL = "    ORDER BY created_at DESC"

# Auditoría — filtros: usuario/detalle (ILIKE), accion/entidad (=), fecha (>=,<=)
SELECT_AUDITORIA_FILTER_BASE = """
    SELECT id, usuario, accion, entidad, entidad_id, detalle, created_at
    FROM auditoria
"""
SELECT_AUDITORIA_FILTER_TAIL = "    ORDER BY created_at DESC"
