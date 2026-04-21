from sqlalchemy import Column, Integer, String, ForeignKey, Date, Float
from sqlalchemy.orm import relationship
from app.models import Base

class Membresia(Base):
    __tablename__ = "membresia"

    id_membresia = Column(Integer, primary_key=True, index=True)
    id_miembro = Column(Integer, ForeignKey("miembro.id_miembro"), nullable=False)
    id_disciplina = Column(Integer, ForeignKey("disciplina.id_disciplina"), nullable=False)
    id_instructor = Column(Integer, ForeignKey("instructor.id_instructor"), nullable=True)
    fecha_inicio = Column(Date, nullable=False)
    fecha_vencimiento = Column(Date, nullable=False)
    # Estado: "nuevo" | "activo" | "vencido"
    estado = Column(String(20), nullable=False, default="nuevo")
    precio_abonado = Column(Float, nullable=False, default=0.0)

    miembro = relationship("Miembro", back_populates="membresias")
    disciplina = relationship("Disciplina")
    instructor = relationship("Instructor", back_populates="membresias")
