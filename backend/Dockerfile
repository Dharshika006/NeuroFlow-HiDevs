FROM python:3.12-slim

# Set working directory

WORKDIR /app

# Copy all files

COPY . .

# Install dependencies

RUN pip install --no-cache-dir fastapi uvicorn asyncpg pydantic-settings redis

# Start the FastAPI server

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

