FROM python:3.11-slim AS builder
WORKDIR /app

RUN apt-get update \
 && apt-get install -y --no-install-recommends gcc libpq-dev \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt setup.py ./

COPY src/      src/
COPY config/   config/
COPY alembic/  alembic/
COPY alembic.ini alembic.ini


RUN python -m venv /opt/venv \
 && /opt/venv/bin/pip install --upgrade pip \
 && /opt/venv/bin/pip install --no-cache-dir -r requirements.txt \
 && /opt/venv/bin/pip install --no-cache-dir -e .

FROM python:3.11-slim
WORKDIR /app

COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY --from=builder /app/src     ./src
COPY --from=builder /app/config  ./config
COPY --from=builder /app/alembic ./alembic
COPY --from=builder /app/alembic.ini ./alembic.ini

COPY entrypoint.sh ./entrypoint.sh
RUN chmod +x ./entrypoint.sh \
 && apt-get update && apt-get install -y --no-install-recommends \
    curl \
    postgresql-client \
 && rm -rf /var/lib/apt/lists/*

EXPOSE 8000

ENTRYPOINT ["./entrypoint.sh"]
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "-w", "4", "--bind", "0.0.0.0:8000", "--log-level", "info", "--access-logfile", "-", "--error-logfile", "-", "adapters.incoming.fastapi.controllers:app"]