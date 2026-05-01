from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select
from datetime import date
from app.config.database import get_db
from app.models.membresia import Membresia
from app.models.gasto import Gasto
from app.schemas.finanzas import DashboardMensualResponse

router = APIRouter(prefix="/api/finanzas", tags=["Finanzas"])

@router.get("/dashboard", response_model=DashboardMensualResponse)
async def obtener_dashboard_mensual(db: AsyncSession = Depends(get_db)):
    hoy = date.today()
    primer_dia_mes = hoy.replace(day=1)

    res_ingresos = await db.execute(
        select(func.sum(Membresia.precio_abonado)).where(
            Membresia.fecha_inicio >= primer_dia_mes
        )
    )
    ingresos = res_ingresos.scalar() or 0.0

    res_insumos = await db.execute(
        select(func.sum(Gasto.monto)).where(
            Gasto.fecha >= primer_dia_mes,
            Gasto.categoria != "sueldos"
        )
    )
    gastos_insumos = res_insumos.scalar() or 0.0

    res_sueldos = await db.execute(
        select(func.sum(Gasto.monto)).where(
            Gasto.fecha >= primer_dia_mes,
            Gasto.categoria == "sueldos"
        )
    )
    gastos_sueldos = res_sueldos.scalar() or 0.0

    total_egresos = gastos_insumos + gastos_sueldos
    ganancia_neta = ingresos - total_egresos

    return {
        "mes": hoy.strftime("%B %Y"),
        "ingresos_totales": ingresos,
        "gastos_insumos": gastos_insumos,
        "pago_instructores": gastos_sueldos,
        "ganancia_neta": ganancia_neta
    }