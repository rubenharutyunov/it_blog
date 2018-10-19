import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

SITE_ID = 2

STATIC_ROOT = os.path.join(BASE_DIR)
STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = "aleximeky@gmail.com"
EMAIL_HOST_PASSWORD = "14885141488514"
EMAIL_USE_TLS = True