FROM python:3.10

#Comento la siguiente linea para hacer pruebas
#ENV DASH_DEBUG_MODE False

# Establecer el directorio de trabajo en /app
WORKDIR /app

# Copiar el archivo de dependencias requirements.txt
COPY requirements.txt requirements.txt

# Instalar las dependencias necesarias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el código de la aplicación (código de Dash, assets, pages, etc.)
COPY . .

# Exponer el puerto 8050 para acceder a la aplicación Dash
EXPOSE 8050

# Establecer el comando para ejecutar la aplicación con Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8050", "--reload", "app:server"]

