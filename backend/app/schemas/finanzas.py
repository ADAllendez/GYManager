from pydantic import BaseModel

class DashboardMensualResponse(BaseModel):
    mes: str
    ingresos_totales: float
    gastos_insumos: float
    pago_instructores: float
    ganancia_neta: float