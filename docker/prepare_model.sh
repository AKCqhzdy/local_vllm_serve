#!/bin/bash
set -e

# Get command line arguments
MODEL_NAME="$1"    # First argument: directory to store the model
PORT="$2"    # Second argument: URL to download the model from
MODEL_DIR="$3"  # Third argument: HuggingFace endpoint
HF_ENDPOINT="$4"  # Fourth argument: HuggingFace token
HUGGING_FACE_HUB_TOKEN="$5"  # Fourth argument: HuggingFace token

# Create a conf.toml file
printf "[model]\nMODEL_NAME = \"%s\"\nPORT = %s\nMODEL_DIR = \"%s\"\n" "$MODEL_NAME" "$PORT" "$MODEL_DIR" > conf.toml

# Set environment variables
export HF_ENDPOINT=${HF_ENDPOINT}
echo "pwd: $(pwd)"

if [ ! -d "$MODEL_DIR" ] || [ -z "$(ls -A "$MODEL_DIR")" ]; then
  echo "Model not found at $MODEL_DIR. Downloading from $MODEL_URL..."
  # Add token authentication to fix 401 Unauthorized error
  if [ -z "$HUGGING_FACE_HUB_TOKEN" ]; then
    echo "Warning: HUGGING_FACE_HUB_TOKEN environment variable not set. Authentication may fail."
  fi
  huggingface-cli download --resume-download "$MODEL_URL" --local-dir "$MODEL_DIR" --token "$HUGGING_FACE_HUB_TOKEN"
else
  echo "Model found at $MODEL_DIR. Skipping download."
fi