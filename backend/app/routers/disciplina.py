from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.config.database import get_db
from app.models.disciplina import Disciplina
from app.schemas.disciplina import DisciplinaIn, DisciplinaOut

router = APIRouter(prefix="/disciplinas", tags=["Disciplinas"])

@router.get("/", response_model=list[DisciplinaOut])
async def listar_disciplinas(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Disciplina))
    return result.scalars().all()

@router.get("/{id_disciplina}", response_model=DisciplinaOut)
async def obtener_disciplina(id_disciplina: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Disciplina).where(Disciplina.id_disciplina == id_disciplina))
    disciplina = result.scalar_one_or_none()
    if not disciplina:
        raise HTTPException(status_code=404, detail="Disciplina no encontrada")
    return disciplina

@router.post("/", response_model=DisciplinaOut)
async def crear_disciplina(datos: DisciplinaIn, db: AsyncSession = Depends(get_db)):
    nueva = Disciplina(**datos.model_dump())
    db.add(nueva)
    await db.commit()
    await db.refresh(nueva)
    return nueva

@router.put("/{id_disciplina}", response_model=DisciplinaOut)
async def actualizar_disciplina(id_disciplina: int, datos: DisciplinaIn, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Disciplina).where(Disciplina.id_disciplina == id_disciplina))
    disciplina = result.scalar_one_or_none()
    if not disciplina:
        raise HTTPException(status_code=404, detail="Disciplina no encontrada")
    for key, value in datos.model_dump().items():
        setattr(disciplina, key, value)
    await db.commit()
    await db.refresh(disciplina)
    return disciplina

@router.delete("/{id_disciplina}")
async def eliminar_disciplina(id_disciplina: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Disciplina).where(Disciplina.id_disciplina == id_disciplina))
    disciplina = result.scalar_one_or_none()
    if not disciplina:
        raise HTTPException(status_code=404, detail="Disciplina no encontrada")
    await db.delete(disciplina)
    await db.commit()
    return {"message": "Disciplina eliminada correctamente"}
