#!/usr/bin/env bash
set -e

docker-compose exec backend python3 manage.py migrate

exit 0