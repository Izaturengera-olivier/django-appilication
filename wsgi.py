import os
import sys

# Add your project directory to the Python path
path = '/home/izyy720/weather-prediction-system'
if path not in sys.path:
    sys.path.insert(0, path)

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.weather_site.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()