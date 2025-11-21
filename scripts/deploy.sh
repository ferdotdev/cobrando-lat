#!/bin/bash

sudo git pull origin main
docker compose -f docker/prod/docker-compose.yml down -v
docker compose -f docker/prod/docker-compose.yml up --build -d
echo "Deployed successfully!"