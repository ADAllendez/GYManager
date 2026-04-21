from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioResponse
import hashlib

router = APIRouter(prefix="/api/usuarios", tags=["Usuarios"])

# Función simple para encriptar la contraseña
def hash_password(password: str):
    return hashlib.sha256(password.encode()).hexdigest()

@router.post("/", response_model=UsuarioResponse)
def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    # 1. Verificar que el nombre de usuario no exista ya
    db_user = db.query(Usuario).filter(Usuario.username == usuario.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="El nombre de usuario ya está en uso")
    
    # 2. Crear el usuario con la contraseña encriptada
    nuevo_usuario = Usuario(
        username=usuario.username,
        password_hash=hash_password(usuario.password),
        rol=usuario.rol
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario