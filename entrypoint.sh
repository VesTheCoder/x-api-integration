#!/bin/sh
set -e

echo "Applying database migrations..."
uv run alembic upgrade head

echo "Starting application..."
exec uv run python app/main.py
