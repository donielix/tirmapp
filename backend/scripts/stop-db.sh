#!/usr/bin/env bash
set -e

usage() { echo "Usage: $0 [-v ]" 1>&2; exit 1; }

ROOT_DIR=$(git rev-parse --show-toplevel)

while getopts vh OPT
do
    case "$OPT" in
        v) v=1 ;;
        *) usage ;;
    esac
done

shift $((OPTIND-1))

if [ -z "$v" ]; then
    docker-compose -f $ROOT_DIR/backend/db/docker-compose.yml down
else
    echo "Removing volumes..."
    docker-compose -f $ROOT_DIR/backend/db/docker-compose.yml down -v
fi