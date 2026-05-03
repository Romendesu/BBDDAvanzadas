from dataclasses import dataclass
from uuid import UUID
import datetime

# ----------------------------------------
# |  Entidades de la base de datos       |
# ----------------------------------------
# | Profesores | PK = ID                 |
# | Alumnos    | PK = ID                 |
# | Cursos     | PK = ID                 |
# | Matriculas | PK = (AlumnoID, CursoID)|
# ----------------------------------------

@dataclass
class Profesores():
    id: UUID
    nombre: str

    def __str__(self):
        return f"ID: {self.id} - NOMBRE: {self.nombre}"
@dataclass
class Alumnos():
    id: UUID
    nombre: str
    email: str

    def __str__(self):
        return f"ID: {self.id} - NOMBRE: {self.nombre} - CORREO: {self.email}"

@dataclass
class Cursos():
    id: UUID
    nombre: str
    profesor_id: UUID


@dataclass
class Matriculas():
    alumno_id: UUID
    curso_id: UUID
    created_at: datetime.datetime

