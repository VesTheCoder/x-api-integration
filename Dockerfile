FROM python:3.14-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/x-api-integration

RUN pip install uv

WORKDIR /x-api-integration

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project

COPY app/ ./app/
COPY alembic.ini ./
COPY alembic/ ./alembic/
COPY entrypoint.sh ./
RUN sed -i 's/\r$//' ./entrypoint.sh && chmod +x ./entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["./entrypoint.sh"]
