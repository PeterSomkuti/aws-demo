#!/bin/bash

# Get needed tools
sudo dnf install curl

# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Source bash again
source ~/.bashrc

# Instantiate project
uv sync

echo "Ready to go!"
