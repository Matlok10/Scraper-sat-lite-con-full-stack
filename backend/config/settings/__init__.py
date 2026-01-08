"""
Selector de configuración basado en variable de entorno.
"""
import os
from .base import *

ENVIRONMENT = os.getenv('DJANGO_ENV', 'development')

if ENVIRONMENT == 'production':
    from .production import *
elif ENVIRONMENT == 'test' or ENVIRONMENT == 'testing':
    from .test import *
else:
    from .development import *
