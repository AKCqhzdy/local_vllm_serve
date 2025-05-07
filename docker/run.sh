#! /bin/bash

# Get the current directory path
CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
# Change to the parent directory (project root)
PROJECT_ROOT="$CURRENT_DIR/.."

# Create models and datasets if not exist
mkdir -p $PROJECT_ROOT/models
mkdir -p $PROJECT_ROOT/datasets

# run on proj54
docker-compose -f $CURRENT_DIR/docker-compose.yml --env-file $CURRENT_DIR/.env up -d