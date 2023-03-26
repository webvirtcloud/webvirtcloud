#!/usr/bin/env bash
set -e

docker compose down
docker rmi webvirtbackend:dev
docker compose up -d

exit 0
