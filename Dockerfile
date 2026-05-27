FROM python:3.14-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/x-api-integration

RUN pip install uv

WORKDIR /x-api-integration

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project

COPY app/ ./

EXPOSE 8000

CMD ["uv", "run", "python", "main.py"]
