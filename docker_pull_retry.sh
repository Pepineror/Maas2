#!/bin/bash

# List of images to pull
IMAGES=(
    "clickhouse/clickhouse-server:24.12"
    "ghcr.io/open-webui/open-webui:main-slim"
    "kong:2.8.1"
    "postgrest/postgrest:v12.0.2"
    "redis:alpine"
    "supabase/gotrue:v2.132.3"
    "supabase/postgres:15.1.1.78"
    "python:3.11-slim-bookworm"
    "python:3.12-slim"
    "agentopsai/otelcontribcol:latest"
)

MAX_RETRIES=10
RETRY_DELAY=5

echo "Starting resilient image pull..."

for img in "${IMAGES[@]}"; do
    SUCCESS=0
    for ((i=1; i<=MAX_RETRIES; i++)); do
        echo "Attempting to pull $img (Try $i/$MAX_RETRIES)..."
        if docker pull "$img"; then
            echo "Successfully pulled $img"
            SUCCESS=1
            break
        else
            echo "Failed to pull $img. Retrying in ${RETRY_DELAY}s..."
            sleep $RETRY_DELAY
        fi
    done

    if [ $SUCCESS -eq 0 ]; then
        echo "Failed to pull $img after $MAX_RETRIES attempts. Exiting."
        exit 1
    fi
done

echo "All images pulled successfully. You can now run: docker-compose up -d --build"
