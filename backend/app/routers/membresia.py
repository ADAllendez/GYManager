from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import date

from app.config.database import get_db
from app.models.membresia import Membresia
from app.models.miembro import Miembro
from app.models.disciplina import Disciplina
from app.models.instructor import Instructor
from app.schemas.membresia import MembresiaIn, MembresiaOut

router = APIRouter(prefix="/membresias", tags=["Membresias"])

# LISTAR todas con datos enriquecidos
@router.get("/", response_model=list[MembresiaOut])
async def listar_membresias(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(
            Membresia,
            Miembro.nombre.label("m_nombre"),
            Miembro.apellido.label("m_apellido"),
            Disciplina.nombre.label("d_nombre"),
            Instructor.nombre.label("i_nombre"),
            Instructor.apellido.label("i_apellido"),
        )
        .join(Miembro, Membresia.id_miembro == Miembro.id_miembro)
        .join(Disciplina, Membresia.id_disciplina == Disciplina.id_disciplina)
        .outerjoin(Instructor, Membresia.id_instructor == Instructor.id_instructor)
    )
    rows = result.all()

    membresias = []
    for mem, m_nombre, m_apellido, d_nombre, i_nombre, i_apellido in rows:
        membresias.append({
            "id_membresia": mem.id_membresia,
            "id_miembro": mem.id_miembro,
            "id_disciplina": mem.id_disciplina,
            "id_instructor": mem.id_instructor,
            "fecha_inicio": mem.fecha_inicio,
            "fecha_vencimiento": mem.fecha_vencimiento,
            "estado": mem.estado,
            "precio_abonado": mem.precio_abonado,
            "nombre_miembro": f"{m_nombre} {m_apellido}",
            "nombre_disciplina": d_nombre,
            "nombre_instructor": f"{i_nombre} {i_apellido}" if i_nombre else None,
        })
    return membresias

# OBTENER por ID
@router.get("/{id_membresia}", response_model=MembresiaOut)
async def obtener_membresia(id_membresia: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Membresia).where(Membresia.id_membresia == id_membresia))
    mem = result.scalar_one_or_none()
    if not mem:
        raise HTTPException(status_code=404, detail="Membresía no encontrada")
    return mem

# CREAR
@router.post("/", response_model=MembresiaOut)
async def crear_membresia(datos: MembresiaIn, db: AsyncSession = Depends(get_db)):
    # Validar miembro
    res = await db.execute(select(Miembro).where(Miembro.id_miembro == datos.id_miembro))
    if not res.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Miembro no encontrado")

    # Validar disciplina
    res = await db.execute(select(Disciplina).where(Disciplina.id_disciplina == datos.id_disciplina))
    disciplina = res.scalar_one_or_none()
    if not disciplina:
        raise HTTPException(status_code=400, detail="Disciplina no encontrada")

    # Validar instructor (si se envió)
    if datos.id_instructor:
        res = await db.execute(select(Instructor).where(Instructor.id_instructor == datos.id_instructor))
        if not res.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Instructor no encontrado")

    # Auto-asignar estado según fechas si no se especificó
    hoy = date.today()
    if datos.estado == "nuevo" and datos.fecha_inicio <= hoy:
        if datos.fecha_vencimiento < hoy:
            datos.estado = "vencido"
        else:
            datos.estado = "activo"

    nueva = Membresia(**datos.model_dump())
    db.add(nueva)
    await db.commit()
    await db.refresh(nueva)
    return nueva

# ACTUALIZAR
@router.put("/{id_membresia}", response_model=MembresiaOut)
async def actualizar_membresia(id_membresia: int, datos: MembresiaIn, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Membresia).where(Membresia.id_membresia == id_membresia))
    mem = result.scalar_one_or_none()
    if not mem:
        raise HTTPException(status_code=404, detail="Membresía no encontrada")
    for key, value in datos.model_dump().items():
        setattr(mem, key, value)
    await db.commit()
    await db.refresh(mem)
    return mem

# RENOVAR membresía (crea una nueva a partir de la actual)
@router.post("/{id_membresia}/renovar", response_model=MembresiaOut)
async def renovar_membresia(id_membresia: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Membresia).where(Membresia.id_membresia == id_membresia))
    mem = result.scalar_one_or_none()
    if not mem:
        raise HTTPException(status_code=404, detail="Membresía no encontrada")

    # Obtener precio de la disciplina
    res_disc = await db.execute(select(Disciplina).where(Disciplina.id_disciplina == mem.id_disciplina))
    disciplina = res_disc.scalar_one_or_none()

    from datetime import timedelta
    hoy = date.today()
    # La nueva membresía empieza desde hoy y dura 30 días
    nueva = Membresia(
        id_miembro=mem.id_miembro,
        id_disciplina=mem.id_disciplina,
        id_instructor=mem.id_instructor,
        fecha_inicio=hoy,
        fecha_vencimiento=hoy + timedelta(days=30),
        estado="activo",
        precio_abonado=disciplina.precio_mensual if disciplina else mem.precio_abonado,
    )
    db.add(nueva)
    await db.commit()
    await db.refresh(nueva)
    return nueva

# ELIMINAR
@router.delete("/{id_membresia}")
async def eliminar_membresia(id_membresia: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Membresia).where(Membresia.id_membresia == id_membresia))
    mem = result.scalar_one_or_none()
    if not mem:
        raise HTTPException(status_code=404, detail="Membresía no encontrada")
    await db.delete(mem)
    await db.commit()
    return {"message": "Membresía eliminada correctamente"}
