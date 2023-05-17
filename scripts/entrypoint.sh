#!/usr/bin/env bash

set -e

RUN_MANAGE_PY='poetry run python -m cooking_core.manage'

echo 'Collecting static files...'
$RUN_MANAGE_PY collectstatic --no-input

echo 'Running migrations...'
$RUN_MANAGE_PY migrate --no-input

exec poetry run daphne cooking_core.project.asgi:application -p 8000 -b 0.0.0.0
