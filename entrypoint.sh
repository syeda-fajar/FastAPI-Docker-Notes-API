#!/bin/bash

# Run migrations
echo "Running alembic migrations..."
alembic upgrade head

# Start Gunicorn
echo "Starting Gunicorn..."
exec gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT