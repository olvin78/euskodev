#Usa una imagen base oficial de Python como base
FROM python:3.9-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /euskodev

# Copia el archivo de requerimientos a la carpeta de trabajo
COPY requirements.txt .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el contenido del directorio actual al directorio de trabajo del contenedor
COPY . .

# Expone el puerto que usará la aplicación
EXPOSE 8000

# Comando para correr la aplicación cuando el contenedor se inicie
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]