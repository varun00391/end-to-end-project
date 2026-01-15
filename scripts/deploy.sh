#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BRANCH="test_branch"
APP_NAME="FastAPI"

echo "=========================="
echo "Deploying $APP_NAME"
echo "=========================="

cd "$PROJECT_DIR"

echo "[1/5] Fetching latest code..."
git fetch origin
git reset --hard origin/$BRANCH

echo "[2/5] Stopping existing containers..."
docker compose down || true

echo "[3/5] Building docker image..."
docker compose build --no-cache

echo "[4/5] Starting containers..."
docker compose up -d

echo "[5/5] Waiting for application to become healthy..."

for i in {1..30}; do
  echo "⏳ Checking health ($i/30)..."
  docker logs pdf_extractor_api --tail=5 || true

  if curl -s http://127.0.0.1:8000/health | grep -q ok; then
    echo "✅ Application is healthy"
    exit 0
  fi

  sleep 5
done

echo "❌ Application failed health check"
docker logs pdf_extractor_api
exit 1

