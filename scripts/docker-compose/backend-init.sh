#!/usr/bin/env bash
set -e

docker compose exec backend python3 manage.py migrate
docker compose exec backend sh -c "python3 manage.py loaddata */fixtures/*.json"

exit 0