from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Optional

@dataclass
class Alumno:
    id_alumno: Optional[int]
    nombre: str
    correo: str
    fecha_nacimiento: date

    @classmethod
    def format_row(cls, row):
        ''' Convierte una row obtenida en una query, en un objeto Alumno '''
        if not row:
            return None
        return cls(
            id_alumno=row[0],
            nombre=row[1],
            correo=row[2],
            fecha_nacimiento=row[3],
        )

    def to_dict(self):
        return {
            "id_alumno": self.id_alumno,
            "nombre": self.nombre,
            "correo": self.correo,
            "fecha_nacimiento": self.fecha_nacimiento.isoformat() if self.fecha_nacimiento else None
        }

@dataclass
class Profesor:
    id_profesor: int
    nombre: str
    correo: str
    especialidad: str
    fecha_contratacion: date

    @classmethod
    def from_row(cls, row):
        """Convierte una fila de la BD (tupla) en un objeto Profesor."""
        if not row:
            return None
        return cls(
            id_profesor=row[0],
            nombre=row[1],
            correo=row[2],
            especialidad=row[3],
            fecha_contratacion=row[4]
        )
    
    def to_dict(self) -> dict:
        return {
            "id_profesor": self.id_profesor,
            "nombre": self.nombre,
            "especialidad": self.especialidad,
            "correo":self.correo,
            "fecha_contratacion": self.fecha_contratacion.isoformat() if self.fecha_contratacion else None
        }

@dataclass
class Curso:
    id_curso: Optional[int]
    nombre_curso: str
    id_profesor: Optional[int]  

    @classmethod
    def from_row(cls, row):
        """Convierte una fila de la BD (tupla) en un objeto Curso."""
        if not row:
            return None
        return cls(
            id_curso=row[0],
            nombre_curso=row[1],
            id_profesor=row[2]
        )
    
    def to_dict(self) -> dict:
        return {
            "id_curso": self.id_curso,
            "nombre_curso": self.nombre_curso,
            "id_profesor":self.id_profesor,
        }

@dataclass
class Matricula:
    id_curso: int
    id_alumno: int
    fecha_inscripcion: date
    nota_final: Optional[Decimal] 
    @classmethod
    def from_row(cls, row):
        """Convierte una fila de la BD (tupla) en un objeto Curso."""
        if not row:
            return None
        return cls(
            id_curso=row[0],
            id_alumno=row[1],
            fecha_inscripcion=row[2],
            nota_final=row[3]
        )