from hongaeting.settings.base import *


PROFILE = 'Local'

DEBUG = True

CORS_ORIGIN_ALLOW_ALL = True

CORS_ORIGIN_WHITELIST = (
    'https://localhost:3000',
    'https://127.0.0.1:3000',
    'http://localhost:3000',
    'http://127.0.0.1:3000',
)


# front app url
FRONT_END_URL = 'http://localhost:3000/'


# email setting
EMAIL_HOST = os.environ['EMAIL_HOST']
EMAIL_PORT = os.environ['EMAIL_PORT']
EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
EMAIL_USE_TLS = os.environ['EMAIL_USE_TLS']
