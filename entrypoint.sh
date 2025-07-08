#!/bin/sh

echo "Waiting for the database to start..."
while ! pg_isready -h ${DB_HOST} -p ${DB_PORT:-5432} -U ${DB_USER} > /dev/null 2>&1; do
  echo "Database is unavailable - waiting..."
  sleep 2
done

echo "Database is up - running Alembic migrations..."
alembic upgrade head

echo "Starting the application..."
exec "$@"