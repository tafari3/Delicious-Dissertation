FROM python:3.12-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
COPY pyproject.toml uv.lock ./
RUN pip install --no-cache-dir uv==0.8.17 && uv sync --frozen --no-dev
COPY . .
RUN uv run alembic upgrade head
EXPOSE 8000
CMD ["uv","run","uvicorn","delicious_scanner.app:app","--host","0.0.0.0","--port","8000"]
