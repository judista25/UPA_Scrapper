#!/bin/bash

set -e

VENV_DIR=".venv"
PYTHON_CMD="python3"

echo "Build Script - Setting up env for python"
echo "========================================"

# Check if Python 3 is installed
if ! command -v $PYTHON_CMD &> /dev/null; then
    echo "Python 3 is not installed. Please install Python 3 first."
    exit 1
fi


# Create virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating venv"
    $PYTHON_CMD -m venv $VENV_DIR
else
    echo "Venv already exists"
fi

# Activate virtual environment
echo "Activate venv."
source $VENV_DIR/bin/activate

# Upgrade pip
echo "Upgrade pip."
pip install --upgrade pip > /dev/null 2>&1

# Install requirements
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt > /dev/null 2>&1
    echo "Installed requirements from requirements.txt."
fi

echo ""
echo "✅ Build completed successfully!"
echo ""
echo "To run the scraper, use: ./run.sh"