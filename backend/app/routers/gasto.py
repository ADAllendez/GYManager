from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.config.database import get_db
from app.models.gasto import Gasto
from app.schemas.gasto import GastoCreate, Gasto as GastoSchema

router = APIRouter(prefix="/api/gastos", tags=["Gastos"])

@router.post("/", response_model=GastoSchema)
async def crear_gasto(gasto: GastoCreate, db: AsyncSession = Depends(get_db)):
    nuevo_gasto = Gasto(**gasto.model_dump())
    db.add(nuevo_gasto)
    await db.commit()
    await db.refresh(nuevo_gasto)
    return nuevo_gasto

@router.get("/", response_model=List[GastoSchema])
async def obtener_gastos(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Gasto).order_by(Gasto.fecha.desc()))
    return result.scalars().all()