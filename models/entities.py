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

@dataclass
class Alumnos():
    id: UUID
    nombre: str
    email: str

@dataclass
class Cursos():
    id: UUID
    nombre: str
    profesor_id: Profesores

@dataclass
class Matriculas():
    alumno_id: Alumnos
    curso_id: Cursos
    created_at: datetime.datetime

