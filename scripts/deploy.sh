#!/bin/bash
set -e

#---------------------
# CONFIGURATION
#---------------------

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
# PROJECT_DIR="$HOME/end-to-end-project"
BRANCH="test_branch"
APP_NAME="FastAPI"

echo "=========================="
echo "Deploying $APP_NAME"
echo "=========================="

#-------------------------------
# GO TO PROJECT DIRECTORY
#-------------------------------

if [ ! -d "$PROJECT_DIR" ]; then
   echo " Project directory not found: $PROJECT_DIR"
   exit 1
fi 

cd "$PROJECT_DIR"

#-------------------------------
# Update Code
#-------------------------------

echo "[1/5] Fetching latest code..."
git fetch origin
git reset --hard origin/$BRANCH

#------------------------------
# STOPPING EXISTING CONTAINERS
#------------------------------

echo "[2/5] Stopping existing containers..."
docker-compose down

#-----------------------------
# Build Fresh Image
#-----------------------------

echo "[3/5] Building docker image (no cache)..."
docker-compose build --no-cache

#-----------------------------
# Starting Containers
#-----------------------------

echo "[4/5] Starting containers..."
docker-compose up -d

#----------------------------
# HEALTH CHECK 
#----------------------------

echo "[5/5] Checking application health... "
curl -f http://localhost/health

echo "Deployment completed successfully"
