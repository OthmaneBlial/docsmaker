#!/bin/bash

set -e  # Exit on any error

# Function to print usage
usage() {
    echo "Usage: $0 [--serve]"
    echo "  --serve  Serve the documentation after building"
    exit 1
}

# Parse arguments
SERVE=false
if [ "$1" = "--serve" ]; then
    SERVE=true
elif [ $# -gt 0 ]; then
    usage
fi

# Delete existing site directory
if [ -d "site" ]; then
    echo "Deleting existing site directory..."
    rm -rf site
fi

# Run docsmaker build
echo "Building documentation..."
if ! docsmaker build; then
    echo "Error: docsmaker build failed"
    exit 1
fi

# Optionally serve
if [ "$SERVE" = true ]; then
    echo "Serving documentation..."
    if ! docsmaker serve; then
        echo "Error: Failed to serve documentation"
        exit 1
    fi
fi

echo "Documentation generation complete."