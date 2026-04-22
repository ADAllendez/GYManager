from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioResponse
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta

router = APIRouter(prefix="/api/usuarios", tags=["Usuarios"])

# Configuración de Seguridad y JWT
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "gym_manager_clave_super_secreta" # En producción usar variables de entorno (.env)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 # El token dura 1 día (24 horas)

# Funciones auxiliares de seguridad
def hash_password(password: str):
    return pwd_context.hash(password)

def verificar_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def crear_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


@router.post("/", response_model=UsuarioResponse)
def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    # 1. Verificar que el username no exista
    db_user = db.query(Usuario).filter(Usuario.username == usuario.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="El nombre de usuario ya está en uso")
    
    # 2. Crear usuario
    nuevo_usuario = Usuario(
        username=usuario.username,
        password_hash=hash_password(usuario.password),
        rol=usuario.rol
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario


@router.post("/login")
def login(datos: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # 1. Buscar usuario
    user = db.query(Usuario).filter(Usuario.username == datos.username).first()
    
    # 2. Verificar existencia y contraseña
    if not user or not verificar_password(datos.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Credenciales incorrectas")
    
    # 3. Generar el Token con ID y Rol
    token_data = {
        "sub": user.username,
        "rol": user.rol,
        "id": user.id_usuario
    }
    token = crear_access_token(token_data)
    
    return {"access_token": token, "token_type": "bearer"}