from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config.database import engine, Base

# Importar modelos para que SQLAlchemy los registre antes del create_all
from app.models import miembro, disciplina, instructor, membresia  # noqa

from app.routers import miembro as r_miembro
from app.routers import disciplina as r_disciplina
from app.routers import instructor as r_instructor
from app.routers import membresia as r_membresia

app = FastAPI(
    title="GYM Manager",
    description="Sistema de gestión de miembros y membresías para gimnasio",
    version="1.0.0"
)

# Configuración CORS
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Crear tablas al iniciar (SQLite las crea en el archivo gym.db automáticamente)
@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Incluir routers
app.include_router(r_miembro.router)
app.include_router(r_disciplina.router)
app.include_router(r_instructor.router)
app.include_router(r_membresia.router)

@app.get("/")
async def root():
    return {"message": "Bienvenido a GYM Manager API"}
