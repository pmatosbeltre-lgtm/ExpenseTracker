from pydantic import BaseModel
from datetime import date

# Esquema base con los datos del gasto
class GastoBase(BaseModel):
    concepto: str
    monto: float
    tipo: str  # "ingreso" o "gasto"
    fecha: date

# Para crear un nuevo gasto
class GastoCreate(GastoBase):
    pass

# Para responder al cliente (incluye el ID que genera la BD)
class GastoResponse(GastoBase):
    id: int

    class Config:
        from_attributes = True