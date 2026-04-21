from pydantic import BaseModel
from datetime import date
from typing import Optional

class MembresiaIn(BaseModel):
    id_miembro: int
    id_disciplina: int
    id_instructor: Optional[int] = None
    fecha_inicio: date
    fecha_vencimiento: date
    estado: str = "nuevo"
    precio_abonado: float = 0.0

class MembresiaOut(BaseModel):
    id_membresia: int
    id_miembro: int
    id_disciplina: int
    id_instructor: Optional[int] = None
    fecha_inicio: date
    fecha_vencimiento: date
    estado: str
    precio_abonado: float

    # Datos enriquecidos
    nombre_miembro: Optional[str] = None
    nombre_disciplina: Optional[str] = None
    nombre_instructor: Optional[str] = None

    class Config:
        from_attributes = True
