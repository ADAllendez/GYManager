from pydantic import BaseModel
from typing import Optional

class InstructorIn(BaseModel):
    nombre: str
    apellido: str
    telefono: Optional[str] = None
    id_disciplina: Optional[int] = None

class InstructorOut(InstructorIn):
    id_instructor: int

    class Config:
        from_attributes = True
