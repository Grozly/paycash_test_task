#!/bin/bash
poetry run alembic revision --autogenerate -m "init"
alembic upgrade heads
uvicorn app.main:app --proxy-headers --host 0.0.0.0 --port 8000
