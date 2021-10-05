#!/bin/bash

sleep 10

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")"/.. >/dev/null 2>&1 && pwd)"

cd "${PROJECT_DIR}" || exit 1

make migrate

echo "MIGRATIONS APPLIED"

make loaddata

echo "DATA LOADED"

make superuser

echo "SUPERUSER CREATED: USERNAME: admin, PASSWORD: admin"

make test

make runserver

echo "RUNNING WEB"