#!/bin/bash

set -e

VENV_DIR=".venv"
URL_SCRAPER="get_urls.py"
PRODUCT_SCRAPER="get_product_info.py"
URL_FILE="url_test.txt"

# Check if virtual environment exists
if [ ! -d "$VENV_DIR" ]; then
    echo "❌ Virtual environment not found. Please run ./build.sh first."
    exit 1
fi

# Activate virtual environment
source $VENV_DIR/bin/activate


if [ ! -f "$URL_SCRAPER" ]; then
    echo "Script $URL_SCRAPER not found!"
    exit 1
fi
# Step 1: Scrape product urls and save the to url_test.txt

python $URL_SCRAPER > $URL_FILE

# Step 2: Process first 10 URLs

if [ ! -f "$PRODUCT_SCRAPER" ]; then
    echo "Script $PRODUCT_SCRAPER not found!"
    exit 1
fi

# Read first 10 URLs and process them
head $URL_FILE | python $PRODUCT_SCRAPER


