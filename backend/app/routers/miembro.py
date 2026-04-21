from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from app.config.database import get_db
from app.models.miembro import Miembro
from app.schemas.miembro import MiembroIn, MiembroOut

router = APIRouter(prefix="/miembros", tags=["Miembros"])

# LISTAR TODOS
@router.get("/", response_model=List[MiembroOut])
async def listar_miembros(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Miembro))
    return result.scalars().all()

# OBTENER POR ID
@router.get("/{id_miembro}", response_model=MiembroOut)
async def obtener_miembro(id_miembro: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Miembro).where(Miembro.id_miembro == id_miembro))
    miembro = result.scalar_one_or_none()
    if not miembro:
        raise HTTPException(status_code=404, detail="Miembro no encontrado")
    return miembro

# CREAR
@router.post("/", response_model=MiembroOut)
async def crear_miembro(datos: MiembroIn, db: AsyncSession = Depends(get_db)):
    nuevo = Miembro(**datos.model_dump())
    db.add(nuevo)
    await db.commit()
    await db.refresh(nuevo)
    return nuevo

# ACTUALIZAR
@router.put("/{id_miembro}", response_model=MiembroOut)
async def actualizar_miembro(id_miembro: int, datos: MiembroIn, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Miembro).where(Miembro.id_miembro == id_miembro))
    miembro = result.scalar_one_or_none()
    if not miembro:
        raise HTTPException(status_code=404, detail="Miembro no encontrado")
    for key, value in datos.model_dump().items():
        setattr(miembro, key, value)
    await db.commit()
    await db.refresh(miembro)
    return miembro

# ELIMINAR
@router.delete("/{id_miembro}")
async def eliminar_miembro(id_miembro: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Miembro).where(Miembro.id_miembro == id_miembro))
    miembro = result.scalar_one_or_none()
    if not miembro:
        raise HTTPException(status_code=404, detail="Miembro no encontrado")
    await db.delete(miembro)
    await db.commit()
    return {"message": "Miembro eliminado correctamente"}
