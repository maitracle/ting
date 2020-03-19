from hongaeting.settings.base import *


PROFILE = 'Production'

DEBUG = False

ALLOWED_HOSTS = ['*']

# CORS
CORS_ORIGIN_ALLOW_ALL = True


# Build paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_DIR = os.path.dirname(BASE_DIR)


# static files
STATIC_URL = '/static/'
STATIC_DIR = os.path.join(BASE_DIR, 'static')

# Todo(maitracle): static file dir에 static root가 포함되면 안되는 지 확인한다.
STATICFILES_DIRS = [
    # STATIC_DIR,
]

STATIC_ROOT = os.path.join(BASE_DIR, 'static')


# media files
DEFAULT_FILE_STORAGE = 'common.custom_storages.MediaStorage'
MEDIA_ROOT = 'production/media'


# front app url
FRONT_END_URL = 'http://camcou-front.s3-website-ap-northeast-1.amazonaws.com/'


# email setting
EMAIL_HOST = os.environ['EMAIL_HOST']
EMAIL_PORT = os.environ['EMAIL_PORT']
EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
EMAIL_USE_TLS = os.environ['EMAIL_USE_TLS']
