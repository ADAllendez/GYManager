from pydantic import BaseModel

class UsuarioBase(BaseModel):
    username: str
    rol: str = "admin" # Por defecto será admin, pero le pasaremos "root"

class UsuarioCreate(UsuarioBase):
    password: str

class UsuarioResponse(UsuarioBase):
    id_usuario: int

    class Config:
        from_attributes = True