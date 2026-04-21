from pydantic import BaseModel
from typing import Optional

class DisciplinaIn(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    precio_mensual: float = 0.0

class DisciplinaOut(DisciplinaIn):
    id_disciplina: int

    class Config:
        from_attributes = True
