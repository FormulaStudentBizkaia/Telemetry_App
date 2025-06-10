FROM python:3.10-slim

WORKDIR /app

# Instalar dependencias
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código
COPY recepcion.py .

# Ejecutar el script
CMD ["python", "recepcion.py"]
