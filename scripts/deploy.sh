#!/bin/bash

echo "Updating the repo"
sudo git pull origin main
echo "Taking down the old container"
docker compose -f docker/prod/compose.yaml down -v
echo "Building the new container"
docker compose -f docker/prod/compose.yaml up --build -d
echo "Deployed successfully!"