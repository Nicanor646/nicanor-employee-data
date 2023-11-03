#!/bin/sh
# Create a python virtual environment
echo "Creating virtual environment called apienv"
python3 -m venv apienv
# Activate the virtual environment
echo "Activating virtual environment"
source apienv/bin/activate
# Install the required libraries
pip install -r requirements.txt
