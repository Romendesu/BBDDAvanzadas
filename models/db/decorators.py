from functools import wraps
import psycopg2
from config import (
    PG_HOST, PG_NAME, PG_PASSWORD, PG_PORT, PG_USER
)
# Operaciones de lectura
def with_cursor(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        conn = None
        try:
            conn = psycopg2.connect(
                host=PG_HOST,
                database=PG_NAME,
                user=PG_USER,
                password=PG_PASSWORD,
                port=PG_PORT,
            )
            conn.autocommit = True
            
            cursor = conn.cursor()
            result = f(*args, cursor, **kwargs)
            return result

        except (Exception, psycopg2.DatabaseError) as e:
            print("Error:", e)
        
        finally:
            if conn is not None: conn.close()
    return wrapper

# Operaciones con transacciones -> Rollbacks / Commit
def with_transactions(f):
    ...