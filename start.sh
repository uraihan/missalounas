#!/bin/bash
set -e

source /app/.venv/bin/activate
echo "Checking database..."
uv run src/app/db_check.py
echo "check complete"
echo "Starting webserver"

case $DEPLOY_ENV in
    PROD)
        echo "Starting Gunicorn..."
        exec uv run gunicorn --bind 0.0.0.0:5000 main:app
        ;;
    DEV)
        echo "Starting Flask development server..."
        exec uv run flask --app main run --host=0.0.0.0 --debug
        ;;
    *)
        echo -n "Unknown ENVIRONMENT env variable (PROD or DEV)"
        ;;
esac
