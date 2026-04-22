from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date
from app.config.database import get_db
from app.models.membresia import Membresia
from app.models.gasto import Gasto
from app.schemas.finanzas import DashboardMensualResponse # <-- Importamos el schema

router = APIRouter(prefix="/api/finanzas", tags=["Finanzas"])

# Añadimos el response_model aquí
@router.get("/dashboard", response_model=DashboardMensualResponse) 
def obtener_dashboard_mensual(db: Session = Depends(get_db)):
    hoy = date.today()
    primer_dia_mes = hoy.replace(day=1)
    
    ingresos = db.query(func.sum(Membresia.precio_abonado)).filter(
        Membresia.fecha_inicio >= primer_dia_mes
    ).scalar() or 0.0

    gastos_insumos = db.query(func.sum(Gasto.monto)).filter(
        Gasto.fecha >= primer_dia_mes,
        Gasto.categoria != "sueldos"
    ).scalar() or 0.0

    gastos_sueldos = db.query(func.sum(Gasto.monto)).filter(
        Gasto.fecha >= primer_dia_mes,
        Gasto.categoria == "sueldos"
    ).scalar() or 0.0

    total_egresos = gastos_insumos + gastos_sueldos
    ganancia_neta = ingresos - total_egresos

    # Devolvemos el diccionario que hace match con el Schema
    return {
        "mes": hoy.strftime("%B %Y"),
        "ingresos_totales": ingresos,
        "gastos_insumos": gastos_insumos,
        "pago_instructores": gastos_sueldos,
        "ganancia_neta": ganancia_neta
    }

@router.post("/cerrar-mes")
def ejecutar_cierre_mensual(db: Session = Depends(get_db)):
    # 1. Calculamos los datos del mes actual (mismo código de sumas que ya tienes)
    # ... (ingresos, gastos_insumos, gastos_sueldos) ...
    
    # 2. Creamos el registro del Snapshot
    nuevo_cierre = CierreFinanciero(
        periodo = date.today().strftime("%Y-%m"),
        tipo = "mensual",
        total_ingresos = ingresos,
        total_egresos = gastos_insumos + gastos_sueldos,
        balance_neto = ingresos - (gastos_insumos + gastos_sueldos)
    )
    
    db.add(nuevo_cierre)
    db.commit()
    return {"message": "Cierre mensual guardado con éxito"}