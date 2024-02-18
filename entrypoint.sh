#!/bin/sh

alembic upgrade head

# Run the original CMD (command) specified in the Dockerfile
exec "$@"
