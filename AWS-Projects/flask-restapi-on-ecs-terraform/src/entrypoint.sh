#!/bin/sh

# Initialize and run database migrations
flask db init
flask db migrate -m "Initial migration."
flask db upgrade

# Run the Flask application
exec "$@"
