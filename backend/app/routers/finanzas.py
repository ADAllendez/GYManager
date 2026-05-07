from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select
from datetime import date
from app.config.database import get_db
from app.models.membresia import Membresia
from app.models.gasto import Gasto
from app.schemas.finanzas import DashboardMensualResponse

router = APIRouter(prefix="/api/finanzas", tags=["Finanzas"])

@router.get("/dashboard", response_model=DashboardMensualResponse)
async def obtener_dashboard_mensual(
    anio: int = Query(default=None),
    mes: int  = Query(default=None),
    db: AsyncSession = Depends(get_db)
):
    hoy = date.today()
    if anio is None:
        anio = hoy.year
    if mes is None:
        mes = hoy.month

    primer_dia = date(anio, mes, 1)
    if mes == 12:
        ultimo_dia = date(anio + 1, 1, 1)
    else:
        ultimo_dia = date(anio, mes + 1, 1)

    res_ingresos = await db.execute(
        select(func.sum(Membresia.precio_abonado)).where(
            Membresia.fecha_inicio >= primer_dia,
            Membresia.fecha_inicio < ultimo_dia,
        )
    )
    ingresos = res_ingresos.scalar() or 0.0

    res_insumos = await db.execute(
        select(func.sum(Gasto.monto)).where(
            Gasto.fecha >= primer_dia,
            Gasto.fecha < ultimo_dia,
            Gasto.categoria != "sueldos"
        )
    )
    gastos_insumos = res_insumos.scalar() or 0.0

    res_sueldos = await db.execute(
        select(func.sum(Gasto.monto)).where(
            Gasto.fecha >= primer_dia,
            Gasto.fecha < ultimo_dia,
            Gasto.categoria == "sueldos"
        )
    )
    gastos_sueldos = res_sueldos.scalar() or 0.0

    total_egresos = gastos_insumos + gastos_sueldos
    ganancia_neta = ingresos - total_egresos

    import locale
    try:
        locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")
    except Exception:
        pass
    nombre_mes = primer_dia.strftime("%B %Y").capitalize()

    return {
        "mes": nombre_mes,
        "ingresos_totales": ingresos,
        "gastos_insumos": gastos_insumos,
        "pago_instructores": gastos_sueldos,
        "ganancia_neta": ganancia_neta
    }
