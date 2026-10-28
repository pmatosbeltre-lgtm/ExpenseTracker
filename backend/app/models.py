from sqlalchemy import Column, Integer, String, Float, Date
from app.database import Base

class GastoModel(Base):
    __tablename__ = "gastos"

    id = Column(Integer, primary_key=True, index=True)
    concepto = Column(String, nullable=False)
    # Campo opcional para no romper registros creados antes de esta columna.
    concepto2 = Column(String, nullable=True, default="")
    monto = Column(Float, nullable=False)
    tipo = Column(String, nullable=False)
    fecha = Column(Date, nullable=False)
