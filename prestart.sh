#!/bin/sh

echo "Running database migrations..."
alembic upgrade head
echo "Migrations complete!"
