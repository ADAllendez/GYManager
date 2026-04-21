from pydantic import BaseModel
from datetime import date

class GastoBase(BaseModel):
    concepto: str
    categoria: str
    monto: float
    fecha: date

class GastoCreate(GastoBase):
    pass

class Gasto(GastoBase):
    id_gasto: int

    class Config:
        from_attributes = True