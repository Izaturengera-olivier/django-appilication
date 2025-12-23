#!/bin/bash
# Run these commands in PythonAnywhere console

# 1. Extract the zip file
cd ~
unzip weather-prediction-system.zip

# 2. Install dependencies
cd ~/weather-prediction-system
pip3.10 install --user -r requirements.txt

# 3. Set up Django
cd web
python3.10 manage.py migrate
python3.10 manage.py collectstatic --noinput

# 4. Create superuser (you'll be prompted for username/password)
python3.10 manage.py createsuperuser

# 5. Train the model
cd ..
python3.10 train.py --generate-sample --n-days 365 --model-path model.joblib

echo "Setup complete! Now configure your web app in the PythonAnywhere dashboard."