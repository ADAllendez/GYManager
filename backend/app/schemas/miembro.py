from pydantic import BaseModel
from typing import Optional
from datetime import date

class MiembroBase(BaseModel):
    nombre: str
    apellido: str
    dni: Optional[str] = None
    correo: Optional[str] = None
    telefono: Optional[str] = None
    fecha_nacimiento: Optional[date] = None

class MiembroIn(MiembroBase):
    pass

class MiembroOut(MiembroBase):
    id_miembro: int

    class Config:
        from_attributes = True
