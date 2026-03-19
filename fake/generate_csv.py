import csv
import random
import os
from faker import Faker

fake = Faker("es_ES")
Faker.seed(42)
random.seed(42)

def generate_csv(dir="./dataset_output"):
    # Si no existe el directorio, se crea de forma automática (puedes especificar el nombre del directorio)
    if not os.path.exists(dir):
        os.makedirs(dir)
        print(f"Directorio '{dir}' creado.")

    # Funcion auxiliar para obtener el directorio
    get_path = lambda filename: os.path.join(dir, filename)

    # 1. PROFESORES (10,000)
    with open(get_path('profesores.csv'), 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for i in range(1, 10001):
            writer.writerow([i, fake.name(), fake.ascii_safe_email(), fake.job(), "2024-01-01"])

    # 2. CURSOS (150,000)
    with open(get_path('cursos.csv'), 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for i in range(1, 150001):
            p_id = random.randint(1, 10000)
            writer.writerow([i, f"Curso {i}", p_id])

    # 3. ALUMNOS (1,000,000)
    with open(get_path('alumnos.csv'), 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for i in range(1, 1000001):
            writer.writerow([i, fake.name(), fake.ascii_safe_email(), "2000-01-01"])

    # 4. MATRÍCULAS (7,500,000)
    with open(get_path('matriculas.csv'), 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        alumnos_pool = list(range(1, 1000001))
        for c_id in range(1, 150001):
            # Selección de 50 alumnos distintos para este curso
            inscritos = random.sample(alumnos_pool, 50)
            for a_id in inscritos:
                nota = round(random.uniform(1.0, 10.0), 2)
                writer.writerow([c_id, a_id, "2026-02-01", nota])

if __name__ == "__main__":
    print("Iniciando generación de datos...")
    generate_csv()
    print("Archivos CSV creados exitosamente.")