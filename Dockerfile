# Stage 1 - Dependencies

FROM python:3.12-slim AS deps

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir \
    fastapi \
    uvicorn \
    asyncpg \
    pydantic-settings \
    redis

# Stage 2 - Runtime

FROM python:3.12-slim AS runtime

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

RUN groupadd -r neuroflow && useradd -r -g neuroflow neuroflow

WORKDIR /app

COPY --from=deps /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages

COPY --from=deps /usr/local/bin /usr/local/bin

COPY . .

RUN chown -R neuroflow:neuroflow /app

USER neuroflow

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn","backend.main:app","--host","0.0.0.0","--port","8000"]

