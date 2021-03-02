from amdtelecom.settings.base import BASE_DIR
from amdtelecom.settings.base import *

DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = '#p_$i#w56)lc@6a0)nz6&#%)3d8+yy62+-xy9zxa#6on-e!a5&1234567'
SECRET_KEY = '#p_$i#w56)lc@6a0)nz6&#%)3d8+yy62+-xy9zxa#6on-e!a5&'

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

ALLOWED_HOSTS = ['0.0.0.0', '127.0.0.1', 'localhost', '127.0.0.1:8000']