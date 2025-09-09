FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# system deps (build tools + libpq)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev curl git \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - --version 1.8.0
ENV PATH="/root/.local/bin:${PATH}"

# Copy only dependency files first
COPY pyproject.toml poetry.lock* /app/

# Install deps in /opt/venv instead of /app/.venv
RUN poetry config virtualenvs.in-project false \
    && poetry config virtualenvs.path /opt/venv \
    && poetry install --no-interaction --no-ansi --with dev --all-extras \
    && poetry self add poetry-exec-plugin

# Add venv to PATH
ENV PATH="/opt/venv/bin:$PATH"

# Copy the rest of the code (safe now)
COPY . /app

# Ensure entrypoint has exec permission
RUN chmod +x /app/scripts/entrypoint.sh

EXPOSE 8083

ENV PYTHONPATH="/app/src:${PYTHONPATH}"
ENTRYPOINT ["/app/scripts/entrypoint.sh"]
