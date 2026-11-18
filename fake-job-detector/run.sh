#!/bin/bash
# Startup script for Fake Job & Internship Detection Web Application

echo "=========================================================="
echo "    JobGuard: Fake Job & Internship Detection System      "
echo "=========================================================="

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
    echo "Installing required dependencies..."
    .venv/bin/pip install -r requirements.txt
fi

# Check if model artifacts exist
if [ ! -f "models/fake_job_model.pkl" ]; then
    echo "Training machine learning model and building dataset..."
    python3 data/create_dataset.py
    .venv/bin/python train_model.py
fi

echo ""
echo "Starting Flask web application..."
echo "Open your web browser at: http://127.0.0.1:5000"
echo "Press Ctrl+C to stop the server."
echo ""

.venv/bin/python app.py
