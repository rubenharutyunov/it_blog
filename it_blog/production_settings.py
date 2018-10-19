import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
'default': {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'itandwisdom',
    'USER': 'root',
    'PASSWORD': 'C!zz20..',
    'HOST': 'itandwisdom.cxtidprjbx11.eu-west-3.rds.amazonaws.com',
    'PORT': '3306',
    'OPTIONS': {'charset': 'utf8'}, 
    }
}

SITE_ID = 2

STATIC_ROOT = os.path.join(BASE_DIR, "static")
#STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)

#EMAIL_HOST = 'email-smtp.eu-west-1.amazonaws.com'
#EMAIL_PORT = 587
#EMAIL_HOST_USER = "AKIAI46AGGPWT54ZGHCA"
#EMAIL_HOST_PASSWORD = "AngP+08dpOKC7cCt0jmEp6l6+BqKjHEGIEVChOuqVIaz"
#EMAIL_USE_TLS = True

EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_PORT = 587
EMAIL_HOST_USER = "no-reply@itandwisdom.com"
EMAIL_HOST_PASSWORD = "N0=,A1Gj"
EMAIL_USE_TLS = True
