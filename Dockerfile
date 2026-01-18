FROM python:3.12-slim AS builder
WORKDIR /app
RUN apt-get update && apt-get install --no-install-recommends -y \
    gcc \
    libpq-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:0.9.22 /uv /bin/

COPY pyproject.toml uv.lock ./

RUN python -m venv .venv \
    && uv sync --no-group dev

FROM builder
WORKDIR /app
RUN apt-get update && apt-get install --no-install-recommends -y libpq5 \
    && rm -rf /var/lib/apt/lists/*
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
COPY --from=builder /app/.venv /app/.venv
COPY . .
CMD ["python", "-m", "gunicorn", "conf.wsgi", "-b","0.0.0.0:8000"]