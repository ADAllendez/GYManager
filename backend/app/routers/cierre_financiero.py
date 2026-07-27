from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List, Optional
from datetime import date, datetime
from app.config.database import get_db
from app.models.cierre_financiero import CierreFinanciero
from app.models.membresia import Membresia
from app.models.gasto import Gasto
from app.models.pago_dia import PagoDia
from app.schemas.cierre_financiero import CierreFinancieroCreate, CierreFinancieroResponse

router = APIRouter(prefix="/api/cierres", tags=["Cierres Financieros"])


@router.post("/mensual", response_model=CierreFinancieroResponse)
async def ejecutar_cierre_mensual(
    anio: int = Query(...),
    mes: int = Query(...),
    db: AsyncSession = Depends(get_db),
):
    """Ejecuta el cierre financiero mensual para un mes/año dado.
    Calcula ingresos (membresías + pagos día) y egresos (gastos) y los guarda."""

    if not (1 <= mes <= 12):
        raise HTTPException(status_code=400, detail="El mes debe estar entre 1 y 12")
    if not (2000 <= anio <= 2100):
        raise HTTPException(status_code=400, detail="El año debe estar entre 2000 y 2100")

    periodo = f"{anio}-{mes:02d}"

    # Verificar que no exista ya un cierre para este periodo
    existente = await db.execute(
        select(CierreFinanciero).where(
            CierreFinanciero.periodo == periodo,
            CierreFinanciero.tipo == "mensual",
        )
    )
    if existente.scalar_one_or_none():
        raise HTTPException(
            status_code=400,
            detail=f"Ya existe un cierre mensual para {periodo}. Eliminalo primero si querés rehacerlo.",
        )

    primer_dia = date(anio, mes, 1)
    if mes == 12:
        ultimo_dia = date(anio + 1, 1, 1)
    else:
        ultimo_dia = date(anio, mes + 1, 1)

    # Ingresos por membresías
    res_memb = await db.execute(
        select(func.sum(Membresia.precio_abonado)).where(
            Membresia.fecha_inicio >= primer_dia,
            Membresia.fecha_inicio < ultimo_dia,
        )
    )
    ingresos_membresias = res_memb.scalar() or 0.0

    # Ingresos por pagos del día
    res_pagos = await db.execute(
        select(func.sum(PagoDia.monto)).where(
            PagoDia.fecha >= primer_dia,
            PagoDia.fecha < ultimo_dia,
        )
    )
    ingresos_pagos_dia = res_pagos.scalar() or 0.0

    total_ingresos = ingresos_membresias + ingresos_pagos_dia

    # Total egresos (todos los gastos del periodo)
    res_gastos = await db.execute(
        select(func.sum(Gasto.monto)).where(
            Gasto.fecha >= primer_dia,
            Gasto.fecha < ultimo_dia,
        )
    )
    total_egresos = res_gastos.scalar() or 0.0

    balance_neto = total_ingresos - total_egresos

    nuevo_cierre = CierreFinanciero(
        periodo=periodo,
        tipo="mensual",
        total_ingresos=total_ingresos,
        total_egresos=total_egresos,
        balance_neto=balance_neto,
        fecha_ejecucion=datetime.now(),
    )
    db.add(nuevo_cierre)
    await db.commit()
    await db.refresh(nuevo_cierre)
    return nuevo_cierre


@router.get("/", response_model=List[CierreFinancieroResponse])
async def listar_cierres(
    tipo: Optional[str] = Query(default=None),
    db: AsyncSession = Depends(get_db),
):
    """Lista todos los cierres financieros, opcionalmente filtrados por tipo."""
    query = select(CierreFinanciero).order_by(CierreFinanciero.fecha_ejecucion.desc())
    if tipo:
        query = query.where(CierreFinanciero.tipo == tipo)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{id_cierre}", response_model=CierreFinancieroResponse)
async def obtener_cierre(id_cierre: int, db: AsyncSession = Depends(get_db)):
    """Obtiene un cierre financiero por ID."""
    result = await db.execute(
        select(CierreFinanciero).where(CierreFinanciero.id_cierre == id_cierre)
    )
    cierre = result.scalar_one_or_none()
    if not cierre:
        raise HTTPException(status_code=404, detail="Cierre financiero no encontrado")
    return cierre


@router.delete("/{id_cierre}", response_model=CierreFinancieroResponse)
async def eliminar_cierre(id_cierre: int, db: AsyncSession = Depends(get_db)):
    """Elimina un cierre financiero (para poder rehacerlo)."""
    result = await db.execute(
        select(CierreFinanciero).where(CierreFinanciero.id_cierre == id_cierre)
    )
    cierre = result.scalar_one_or_none()
    if not cierre:
        raise HTTPException(status_code=404, detail="Cierre financiero no encontrado")

    try:
        await db.delete(cierre)
        await db.commit()
        return cierre
    except Exception:
        await db.rollback()
        raise HTTPException(status_code=400, detail="No se puede eliminar el cierre financiero")
