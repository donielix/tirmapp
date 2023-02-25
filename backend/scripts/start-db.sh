#!/usr/bin/env bash
set -e

usage() { echo "Usage: $0 [-m ]" 1>&2; exit 1; }

ROOT_DIR=$(git rev-parse --show-toplevel)

while getopts mh OPT
do
    case "$OPT" in
        m) m=1 ;;
        *) usage ;;
    esac
done

shift $((OPTIND-1))

docker-compose -f $ROOT_DIR/backend/db/docker-compose.yml build > /dev/null
docker-compose -f $ROOT_DIR/backend/db/docker-compose.yml up -d

if [ -n "$m" ]; then
    sleep 3
    "${ROOT_DIR}"/backend/venv/bin/python "${ROOT_DIR}"/backend/manage.py makemigrations && \
    "${ROOT_DIR}"/backend/venv/bin/python "${ROOT_DIR}"/backend/manage.py migrate --no-input
fi
