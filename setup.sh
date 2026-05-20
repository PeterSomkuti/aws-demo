#!/bin/bash

# Get needed tools
sudo dnf install curl

# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Instantiate project
uv sync

echo "Ready to go!"
