"""
Configuración para el ambiente de TESTING
"""
from .base import *

# Clave secreta fija para tests
SECRET_KEY = 'test-secret-key-for-recos-project'

DEBUG = False

ALLOWED_HOSTS = ['*']

# Base de datos en memoria para velocidad
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# Deshabilitar logging excesivo durante tests
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'CRITICAL',
    },
}

# Hashers rápidos para tests de usuarios
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]
