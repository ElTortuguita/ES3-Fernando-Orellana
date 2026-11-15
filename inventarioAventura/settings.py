from pathlib import Path
import os
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-aventuras-solo-demostracion-local')
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']
INSTALLED_APPS = [
    'django.contrib.admin', 'django.contrib.auth', 'django.contrib.contenttypes',
    'django.contrib.sessions', 'django.contrib.messages', 'django.contrib.staticfiles',
    'core', 'cuentas', 'experiencias',
]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
ROOT_URLCONF = 'inventarioAventura.urls'
TEMPLATES = [{'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [BASE_DIR / 'templates'], 'APP_DIRS': True,
    'OPTIONS': {'context_processors': [
        'django.template.context_processors.request',
        'django.contrib.auth.context_processors.auth',
        'django.contrib.messages.context_processors.messages',
    ]}}]
WSGI_APPLICATION = 'inventarioAventura.wsgi.application'
DATABASES = {'default': {
    'ENGINE': 'mysql.connector.django',
    'NAME': os.environ.get('MYSQL_DATABASE', 'aventuras_del_sur_db'),
    'USER': os.environ.get('MYSQL_USER', 'root'),
    'PASSWORD': os.environ.get('MYSQL_PASSWORD', ''),
    'HOST': os.environ.get('MYSQL_HOST', '127.0.0.1'),
    'PORT': os.environ.get('MYSQL_PORT', '3306'),
    'OPTIONS': {'use_pure': True, 'charset': 'utf8mb4',
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"},
}}
# Esta copia local se excluye del repositorio y del archivo de entrega.
try:
    from .config_local import MYSQL_PASSWORD
except ImportError:
    pass
else:
    DATABASES['default']['PASSWORD'] = MYSQL_PASSWORD
AUTH_USER_MODEL = 'cuentas.Usuario'
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]
LOGIN_URL = 'cuentas:login'
LOGIN_REDIRECT_URL = 'core:panel'
LOGOUT_REDIRECT_URL = 'core:inicio'
LANGUAGE_CODE = 'es-cl'
TIME_ZONE = 'America/Santiago'
USE_I18N = True
USE_TZ = True
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
