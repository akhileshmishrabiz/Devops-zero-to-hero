#!/bin/sh
set -e

# # Extract host from DATABASE_URL for health check
# get_db_host() {
#     echo "$DB_HOST" | grep -oP '@\K[^:]+' || echo "db"
# }

# # Function to check if database is ready
# check_db() {
#     DB_HOST=$(get_db_host)
#     echo "Checking database connection..."
#     while ! nc -z $DB_HOST 5432; do
#         echo "Database is not available - sleeping"
#         sleep 2
#     done
#     echo "Database is available"
# }

# Check if we need to run migrations
# if [ "$RUN_MIGRATIONS" = "true" ]; then
#     check_db
#     echo "Running database migrations..."
#     flask db upgrade
#     echo "Migrations completed"
#     exit 0
# fi

# For web application container
# check_db
echo "Starting Gunicorn..."
exec gunicorn \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --threads 2 \
    --timeout 60 \
    --access-logfile - \
    --error-logfile - \
    wsgi:app