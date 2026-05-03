#!/usr/bin/env bash
set -euo pipefail

COMPOSE_FILES=(
  -f compose.yaml
  -f compose.local.yaml
  -f compose.direct-sql.yaml
  -f compose.prism-toy.yaml
)

docker compose "${COMPOSE_FILES[@]}" down -v >/dev/null 2>&1 || true

docker compose "${COMPOSE_FILES[@]}" up --build -d database importer

IMPORTER_ID="$(docker compose "${COMPOSE_FILES[@]}" ps -aq importer)"

if [ -z "$IMPORTER_ID" ]; then
  echo "Importer container not found."
  docker compose "${COMPOSE_FILES[@]}" ps
  exit 1
fi

docker wait "$IMPORTER_ID" >/dev/null

python3 generate_prism_qa_report.py

cat reports/prism_qa_report.md

docker compose "${COMPOSE_FILES[@]}" down -v
