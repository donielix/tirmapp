#!/usr/bin/env bash
set -e

ROOT_DIR=$(git rev-parse --show-toplevel)

docker-compose -f $ROOT_DIR/backend/db/docker-compose.yml build > /dev/null
docker-compose -f $ROOT_DIR/backend/db/docker-compose.yml up -d
