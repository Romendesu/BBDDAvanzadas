"""
DAG de usuarios — Parte B
Pipeline independiente que crea la base de datos SQLite de autenticación
e inserta los usuarios del sistema con contraseñas cifradas.

Usuarios insertados:
    admin   · rol: admin
    profesor · rol: profesor
    alumno  · rol: alumno
"""

from __future__ import annotations

import sqlite3
import os
from datetime import datetime, timedelta

from werkzeug.security import generate_password_hash
from airflow import DAG
from airflow.operators.python import PythonOperator

# ── Ruta de la base de datos SQLite ──────────────────────────────────────────

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SQLITE_PATH = os.path.join(BASE_DIR, "auth.db")

# ── Usuarios a insertar ───────────────────────────────────────────────────────

USUARIOS = [
    {
        "username":    "admin",
        "email":       "admin@academico.es",
        "password":    "Admin1234!",
        "nombre":      "Administrador del Sistema",
        "rol":         "admin",
        "is_active":   1,
    },
    {
        "username":    "profesor",
        "email":       "profesor@academico.es",
        "password":    "Profesor1234!",
        "nombre":      "Profesor Demo",
        "rol":         "profesor",
        "is_active":   1,
    },
    {
        "username":    "alumno",
        "email":       "alumno@academico.es",
        "password":    "Alumno1234!",
        "nombre":      "Alumno Demo",
        "rol":         "alumno",
        "is_active":   1,
    },
]

# ── DDL ───────────────────────────────────────────────────────────────────────

DDL_USUARIOS = """
    CREATE TABLE IF NOT EXISTS usuarios (
        id           INTEGER PRIMARY KEY AUTOINCREMENT,
        username     TEXT    NOT NULL UNIQUE,
        email        TEXT    NOT NULL UNIQUE,
        password_hash TEXT   NOT NULL,
        nombre       TEXT    NOT NULL,
        rol          TEXT    NOT NULL DEFAULT 'alumno'
                             CHECK (rol IN ('admin', 'profesor', 'alumno')),
        is_active    INTEGER NOT NULL DEFAULT 1,
        created_at   TEXT    NOT NULL
    );
"""

DDL_INDEX_USERNAME = """
    CREATE UNIQUE INDEX IF NOT EXISTS idx_usuarios_username ON usuarios (username);
"""

DDL_INDEX_EMAIL = """
    CREATE UNIQUE INDEX IF NOT EXISTS idx_usuarios_email ON usuarios (email);
"""


# ── Tarea 1: comprobar / crear base de datos ──────────────────────────────────

def check_sqlite():
    conn = sqlite3.connect(SQLITE_PATH)
    cur  = conn.cursor()
    cur.execute("SELECT sqlite_version();")
    version = cur.fetchone()[0]
    conn.close()
    print(f"[OK] SQLite {version} — base de datos en: {SQLITE_PATH}")


# ── Tarea 2: crear tabla de usuarios ─────────────────────────────────────────

def create_users_table():
    conn = sqlite3.connect(SQLITE_PATH)
    cur  = conn.cursor()
    try:
        cur.execute(DDL_USUARIOS)
        cur.execute(DDL_INDEX_USERNAME)
        cur.execute(DDL_INDEX_EMAIL)
        conn.commit()
        print("[OK] Tabla 'usuarios' creada / verificada.")
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()


# ── Tarea 3: insertar usuarios con contraseñas cifradas ──────────────────────

def insert_users():
    conn = sqlite3.connect(SQLITE_PATH)
    cur  = conn.cursor()

    try:
        inserted = 0
        skipped  = 0

        for u in USUARIOS:
            cur.execute("SELECT id FROM usuarios WHERE username = ?;", (u["username"],))
            if cur.fetchone():
                print(f"[SKIP] Usuario '{u['username']}' ya existe.")
                skipped += 1
                continue

            password_hash = generate_password_hash(u["password"], method="pbkdf2:sha256")
            cur.execute(
                """INSERT INTO usuarios (username, email, password_hash, nombre, rol, is_active, created_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?);""",
                (
                    u["username"],
                    u["email"],
                    password_hash,
                    u["nombre"],
                    u["rol"],
                    u["is_active"],
                    datetime.utcnow().isoformat(),
                ),
            )
            print(f"[OK] Usuario '{u['username']}' insertado con rol '{u['rol']}'.")
            inserted += 1

        conn.commit()
        print(f"[OK] Resultado: {inserted} insertados, {skipped} omitidos.")

    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()


# ── Definición del DAG ────────────────────────────────────────────────────────

default_args = {
    "owner":            "academico",
    "retries":          1,
    "retry_delay":      timedelta(minutes=2),
    "email_on_failure": False,
}

with DAG(
    dag_id="dag_usuarios_sqlite",
    description="Crea la base de datos SQLite de autenticación e inserta usuarios con contraseñas cifradas.",
    schedule_interval=None,
    start_date=datetime(2024, 1, 1),
    catchup=False,
    default_args=default_args,
    tags=["autenticacion", "sqlite", "usuarios"],
) as dag:

    t1 = PythonOperator(
        task_id="comprobar_sqlite",
        python_callable=check_sqlite,
    )

    t2 = PythonOperator(
        task_id="crear_tabla_usuarios",
        python_callable=create_users_table,
    )

    t3 = PythonOperator(
        task_id="insertar_usuarios",
        python_callable=insert_users,
    )

    t1 >> t2 >> t3
