#!/bin/bash
# Activate virtual environment and run the YouTube to FLAC converter

# Navigate to script directory
cd "$(dirname "$0")"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run:"
    echo "   python3 -m venv venv"
    echo "   source venv/bin/activate"
    echo "   pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Run the script
python youtube_to_flac.py

# Deactivate virtual environment
deactivate
