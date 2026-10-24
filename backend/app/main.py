from fastapi import FastAPI
from app.database import engine, Base

# Crea la tabla 'gastos' en PostgreSQL automáticamente si no existe
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Control de Gastos API")

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Contenedores de FastAPI y PostgreSQL funcionando en Docker"}