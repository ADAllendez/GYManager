from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.config.database import get_db
from app.models.gasto import Gasto
from app.schemas.gasto import GastoCreate, Gasto as GastoSchema

router = APIRouter(prefix="/api/gastos", tags=["Gastos"])

@router.post("/", response_model=GastoSchema)
def crear_gasto(gasto: GastoCreate, db: Session = Depends(get_db)):
    nuevo_gasto = Gasto(**gasto.model_dump())
    db.add(nuevo_gasto)
    db.commit()
    db.refresh(nuevo_gasto)
    return nuevo_gasto

@router.get("/", response_model=List[GastoSchema])
def obtener_gastos(db: Session = Depends(get_db)):
    return db.query(Gasto).order_by(Gasto.fecha.desc()).all()