import os
from .base import *


SECRET_KEY = os.environ["SECRET_KEY"]
DEBUG = False
ALLOWED_HOSTS = ["127.0.0.1", "https://c2f5-2401-4900-628a-761c-e75f-8f01-9260-ccbc.ngrok-free.appc"]

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True