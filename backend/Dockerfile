# 1. Usar una imagen slim (pesa ~150 MB vs los ~1 GB de 'python:3')
# Esto reduce drásticamente el tiempo de build en GitHub Actions y el despliegue en GCP
FROM python:3.11-slim

WORKDIR /app

# 2. Copiar e instalar dependencias (aprovechando la caché de Docker)
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 3. Copiar el resto del código de la aplicación
COPY . .

# 4. Exponer el puerto por defecto que usa GCP Cloud Run (8080)
EXPOSE 8080

# 5. Arrancar el servidor ASGI Uvicorn para FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]