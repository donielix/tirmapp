#!/usr/bin/env bash
set -e

ROOT_DIR=$(git rev-parse --show-toplevel)

find "${ROOT_DIR}" -type d -name ${1-venv} -prune -false \
-o -type f \( -path "*/migrations/*.py" -or -path "*/migrations/*.pyc" \) -not -name "__init__.py" \
-print -exec rm -rf {} \;
