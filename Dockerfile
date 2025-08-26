# Imagen base con Python 3.9
FROM python:3.9-slim

# Evitamos prompts interactivos
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instalamos dependencias del sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Creamos directorio de trabajo
WORKDIR /app

# Copiamos requirements si existen
COPY requirements.txt ./

# Instalamos dependencias de Python
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copiamos el resto del proyecto
COPY . .

# Expone el puerto por defecto de Django
EXPOSE 8000

# Comando para ejecutar el servidor
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
