from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from app.models import Base

class Miembro(Base):
    __tablename__ = "miembro"

    id_miembro = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    dni = Column(String(20), unique=True)
    correo = Column(String(100))
    telefono = Column(String(30))
    fecha_nacimiento = Column(Date, nullable=True)

    membresias = relationship("Membresia", back_populates="miembro")
