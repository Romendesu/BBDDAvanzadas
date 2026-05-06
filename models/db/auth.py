"""
Acceso a la base de datos SQLite de autenticación.
"""
import os
import sqlite3

from werkzeug.security import check_password_hash

BASE_DIR  = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SQLITE_PATH = os.path.join(BASE_DIR, "auth.db")


def _get_conn():
    conn = sqlite3.connect(SQLITE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def get_user_by_username(username: str):
    conn = _get_conn()
    cur  = conn.cursor()
    cur.execute("SELECT * FROM usuarios WHERE username = ? AND is_active = 1;", (username,))
    row = cur.fetchone()
    conn.close()
    return row


def verify_password(username: str, password: str) -> bool:
    user = get_user_by_username(username)
    if not user:
        return False
    return check_password_hash(user["password_hash"], password)
