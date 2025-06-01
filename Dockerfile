FROM python:3.13-slim

WORKDIR /app

RUN python -m pip install uv

COPY pyproject.toml .
COPY uv.lock .

RUN uv sync --no-dev --locked

COPY main.py .
COPY app/ app

CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]