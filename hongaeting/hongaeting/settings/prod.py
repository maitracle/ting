from hongaeting.settings.base import *


PROFILE = 'Production'

DEBUG = False

ALLOWED_HOSTS = ['*']


# Build paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_DIR = os.path.dirname(BASE_DIR)

# static files
STATIC_URL = '/static/'
STATIC_DIR = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [
    STATIC_DIR,
]

STATIC_ROOT = os.path.join(ROOT_DIR, '.static_root')
