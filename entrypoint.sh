
echo "Waiting for postgres..."


while ! nc -z db 5432; do
  sleep 0.1
done

echo "PostgreSQL started"


echo "Running alembic migrations..."
alembic upgrade head


echo "Starting Gunicorn..."
exec gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000