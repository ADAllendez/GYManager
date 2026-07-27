from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class CierreFinancieroCreate(BaseModel):
    periodo: str          # Ej: "2026-06" o "Semana 26-2026"
    tipo: str             # "mensual" o "semanal"
    total_ingresos: float
    total_egresos: float
    balance_neto: float


class CierreFinancieroResponse(BaseModel):
    id_cierre: int
    periodo: str
    tipo: str
    total_ingresos: float
    total_egresos: float
    balance_neto: float
    fecha_ejecucion: Optional[datetime] = None

    class Config:
        from_attributes = True
