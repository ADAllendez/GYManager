from pydantic import BaseModel
from typing import Optional

class UsuarioBase(BaseModel):
    username: str
    rol: str = "admin"

    # Datos del perfil — opcionales para no romper el usuario root
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    edad: Optional[int] = None
    telefono: Optional[str] = None
    correo: Optional[str] = None
    dni: Optional[str] = None
    sueldo_mensual: Optional[float] = None
    fecha_contratacion: Optional[str] = None
    foto: Optional[str] = None

class UsuarioCreate(UsuarioBase):
    password: str

class UsuarioUpdate(BaseModel):
    """Para editar: la password es opcional (si no la mandan, no se cambia)"""
    username: Optional[str] = None
    rol: Optional[str] = None
    password: Optional[str] = None
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    edad: Optional[int] = None
    telefono: Optional[str] = None
    correo: Optional[str] = None
    dni: Optional[str] = None
    sueldo_mensual: Optional[float] = None
    fecha_contratacion: Optional[str] = None
    foto: Optional[str] = None

class UsuarioResponse(UsuarioBase):
    id_usuario: int

    class Config:
        from_attributes = True