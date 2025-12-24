#!/bin/bash
set -e

# Load environment variables if needed (though Docker compose does this)
# export $(grep -v '^#' .env | xargs)

echo "🚀 Starting MAAS Document System..."

# Run migrations (TODO: Implement with alembic if using PostgreSQL)
# alembic upgrade head

# Start uvicorn
exec uvicorn backend.main:app --host 0.0.0.0 --port ${PORT:-8000}
