from sqlalchemy import Column, Integer, String, Float, Date
from app.database import Base

class GastoModel(Base):
    __tablename__ = "gastos"

    id = Column(Integer, primary_key=True, index=True)
    concepto = Column(String, nullable=False)
    monto = Column(Float, nullable=False)
    tipo = Column(String, nullable=False)
    fecha = Column(Date, nullable=False)