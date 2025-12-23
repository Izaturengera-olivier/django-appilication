#!/bin/bash
# Minimal setup for PythonAnywhere with disk constraints

cd ~/weather

# Clean up
rm -rf __pycache__ web_static
find . -name "*.pyc" -delete

# Install minimal packages
pip3.10 install --user Django scikit-learn pandas numpy requests joblib

# Django setup
cd web
python3.10 manage.py migrate
python3.10 manage.py createsuperuser

echo "Basic setup complete. Train model later when needed."