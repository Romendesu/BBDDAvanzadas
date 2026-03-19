import psycopg
import time
import sys
import os

# Ensure the root directory is in sys.path to resolve the 'database' package
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database.psql.config import load_config

def get_database_statistics():
    """
    Calculates exact row counts, query execution time, 
    and physical disk usage for core tables.
    """
    db_config = load_config()
    target_tables = ['profesor', 'alumno', 'curso', 'matricula']
    
    try:
        with psycopg.connect(**db_config) as connection:
            with connection.cursor() as cursor:
                print("DATABASE PERFORMANCE AND VOLUME REPORT")
                print(f"{'TABLE NAME':<15} {'ROW COUNT':>12} {'LATENCY':>10} {'DISK SIZE':>12}")

                total_process_start = time.perf_counter()

                for table in target_tables:
                    # Measuring latency for exact row count
                    query_start = time.perf_counter()
                    cursor.execute(f"SELECT COUNT(*) FROM {table}")
                    exact_count = cursor.fetchone()[0]
                    query_end = time.perf_counter()
                    
                    # Fetching physical size including indexes
                    cursor.execute(f"SELECT pg_size_pretty(pg_total_relation_size('{table}'))")
                    disk_usage = cursor.fetchone()[0]
                    
                    execution_latency = query_end - query_start
                    
                    print(f"{table:<15} {exact_count:>12,} {execution_latency:>9.4f}s {disk_usage:>12}")

                total_process_end = time.perf_counter()
                total_duration = total_process_end - total_process_start
                
                print(f"\nAnalysis completed in {total_duration:.2f} seconds.")

    except Exception as error:
        print(f"Execution Error: {error}")

if __name__ == "__main__":
    get_database_statistics()