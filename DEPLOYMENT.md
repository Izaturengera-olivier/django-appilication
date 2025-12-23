# PythonAnywhere Deployment Guide

## 1. Upload Files
Upload your project to `/home/yourusername/weather-prediction-system/`

## 2. Install Dependencies
In PythonAnywhere console:
```bash
cd ~/weather-prediction-system
pip3.10 install --user -r requirements.txt
```

## 3. Configure Web App
- Go to Web tab in PythonAnywhere dashboard
- Create new web app (Django)
- Set source code: `/home/yourusername/weather-prediction-system`
- Set WSGI file: `/home/yourusername/weather-prediction-system/wsgi.py`

## 4. Static Files
In Web tab, add static files mapping:
- URL: `/static/`
- Directory: `/home/yourusername/weather-prediction-system/web/staticfiles/`

## 5. Environment Variables
In Web tab, add environment variables:
- `SECRET_KEY`: Generate a secure key
- `DEBUG`: `False`
- `WEATHER_API_KEY`: Your OpenWeatherMap API key

## 6. Database Setup
In PythonAnywhere console:
```bash
cd ~/weather-prediction-system/web
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic
```

## 7. Train Model
```bash
cd ~/weather-prediction-system
python train.py --generate-sample --n-days 365 --model-path model.joblib
```

## 8. Update WSGI File
Replace `yourusername` in wsgi.py with your actual username.

## 9. Reload Web App
Click "Reload" button in Web tab.