from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from app.database import engine, Base, SessionLocal
from app.models import GastoModel
from app.schemas import GastoCreate, GastoResponse

# Crea las tablas en PostgreSQL si no existen
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Control de Gastos API")

# Habilitar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://app-frontend-testing.ambitiousdune-385a29b9.eastus.azurecontainerapps.io",
    "https://app-frontend-main.ambitiousdune-385a29b9.eastus.azurecontainerapps.io",
    "http://localhost:3000"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependencia para obtener la sesión de la BD en cada petición
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", tags=["Root"])
def read_root():
    return {"status": "ok", "message": "API de Control de Gastos activa"}

# 1. OBTENER TODOS LOS GASTOS (READ)
@app.get("/gastos", response_model=List[GastoResponse], tags=["Gastos"])
def obtener_gastos(db: Session = Depends(get_db)):
    return db.query(GastoModel).all()

# 2. CREAR UN NUEVO GASTO (CREATE)
@app.post("/gastos", response_model=GastoResponse, status_code=status.HTTP_201_CREATED, tags=["Gastos"])
def crear_gasto(gasto: GastoCreate, db: Session = Depends(get_db)):
    nuevo_gasto = GastoModel(**gasto.model_dump())
    db.add(nuevo_gasto)
    db.commit()
    db.refresh(nuevo_gasto)
    return nuevo_gasto

# 3. ACTUALIZAR UN GASTO (UPDATE)
@app.put("/gastos/{gasto_id}", response_model=GastoResponse, tags=["Gastos"])
def actualizar_gasto(gasto_id: int, gasto_actualizado: GastoCreate, db: Session = Depends(get_db)):
    db_gasto = db.query(GastoModel).filter(GastoModel.id == gasto_id).first()
    if not db_gasto:
        raise HTTPException(status_code=404, detail="Gasto no encontrado")
    
    for key, value in gasto_actualizado.model_dump().items():
        setattr(db_gasto, key, value)
    
    db.commit()
    db.refresh(db_gasto)
    return db_gasto

# 4. ELIMINAR UN GASTO (DELETE)
@app.delete("/gastos/{gasto_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Gastos"])
def eliminar_gasto(gasto_id: int, db: Session = Depends(get_db)):
    db_gasto = db.query(GastoModel).filter(GastoModel.id == gasto_id).first()
    if not db_gasto:
        raise HTTPException(status_code=404, detail="Gasto no encontrado")
    
    db.delete(db_gasto)
    db.commit()
    return None