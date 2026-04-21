from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.config.database import get_db
from app.models.instructor import Instructor
from app.models.disciplina import Disciplina
from app.schemas.instructor import InstructorIn, InstructorOut

router = APIRouter(prefix="/instructores", tags=["Instructores"])

@router.get("/", response_model=list[InstructorOut])
async def listar_instructores(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Instructor))
    return result.scalars().all()

@router.get("/{id_instructor}", response_model=InstructorOut)
async def obtener_instructor(id_instructor: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Instructor).where(Instructor.id_instructor == id_instructor))
    instructor = result.scalar_one_or_none()
    if not instructor:
        raise HTTPException(status_code=404, detail="Instructor no encontrado")
    return instructor

@router.post("/", response_model=InstructorOut)
async def crear_instructor(datos: InstructorIn, db: AsyncSession = Depends(get_db)):
    if datos.id_disciplina:
        res = await db.execute(select(Disciplina).where(Disciplina.id_disciplina == datos.id_disciplina))
        if not res.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Disciplina no válida")
    nuevo = Instructor(**datos.model_dump())
    db.add(nuevo)
    await db.commit()
    await db.refresh(nuevo)
    return nuevo

@router.put("/{id_instructor}", response_model=InstructorOut)
async def actualizar_instructor(id_instructor: int, datos: InstructorIn, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Instructor).where(Instructor.id_instructor == id_instructor))
    instructor = result.scalar_one_or_none()
    if not instructor:
        raise HTTPException(status_code=404, detail="Instructor no encontrado")
    for key, value in datos.model_dump().items():
        setattr(instructor, key, value)
    await db.commit()
    await db.refresh(instructor)
    return instructor

@router.delete("/{id_instructor}")
async def eliminar_instructor(id_instructor: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Instructor).where(Instructor.id_instructor == id_instructor))
    instructor = result.scalar_one_or_none()
    if not instructor:
        raise HTTPException(status_code=404, detail="Instructor no encontrado")
    await db.delete(instructor)
    await db.commit()
    return {"message": "Instructor eliminado correctamente"}
