# Imagen base oficial de Python
FROM python:3.12-slim

# Configuración de directorio
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    build-essential libpq-dev curl && \
    rm -rf /var/lib/apt/lists/*

# Instalar Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

# Copiar archivos de proyecto
COPY pyproject.toml poetry.lock* /app/
RUN poetry install --no-root --only main

# Copiar el código
COPY src/ /app/src
COPY .env /app/.env

# Exponer puerto (el mismo que DEV_PORT)
EXPOSE 8081

# Comando para arrancar FastAPI con Uvicorn
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8081"]
