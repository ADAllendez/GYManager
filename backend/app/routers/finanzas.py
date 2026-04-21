from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date, timedelta
from app.config.database import get_db
from app.models.membresia import Membresia
from app.models.gasto import Gasto

router = APIRouter(prefix="/api/finanzas", tags=["Finanzas"])

@router.get("/dashboard")
def obtener_dashboard_mensual(db: Session = Depends(get_db)):
    # 1. Obtener el mes y año actual
    hoy = date.today()
    primer_dia_mes = hoy.replace(day=1)
    
    # 2. Calcular Ingresos Totales del mes (Sumar precio_abonado de Membresias activas/pagadas este mes)
    ingresos = db.query(func.sum(Membresia.precio_abonado)).filter(
        Membresia.fecha_inicio >= primer_dia_mes
    ).scalar() or 0.0

    # 3. Calcular Gastos de Insumos (Todo lo que NO sea sueldo)
    gastos_insumos = db.query(func.sum(Gasto.monto)).filter(
        Gasto.fecha >= primer_dia_mes,
        Gasto.categoria != "sueldos"
    ).scalar() or 0.0

    # 4. Calcular Pago a Instructores (Solo categoría sueldos)
    gastos_sueldos = db.query(func.sum(Gasto.monto)).filter(
        Gasto.fecha >= primer_dia_mes,
        Gasto.categoria == "sueldos"
    ).scalar() or 0.0

    # 5. Calcular Ganancia Neta
    total_egresos = gastos_insumos + gastos_sueldos
    ganancia_neta = ingresos - total_egresos

    return {
        "mes": hoy.strftime("%B %Y"),
        "ingresos_totales": ingresos,
        "gastos_insumos": gastos_insumos,
        "pago_instructores": gastos_sueldos,
        "ganancia_neta": ganancia_neta
    }