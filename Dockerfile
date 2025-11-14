# Based on https://docs.astral.sh/uv/guides/integration/fastapi/
FROM python:3.13-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY .python-version pyproject.toml uv.lock /app/

WORKDIR /app

RUN uv sync --frozen --no-cache

COPY src /app/src

CMD ["uv", "run", "src/main.py"]
