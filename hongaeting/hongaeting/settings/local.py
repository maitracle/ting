from hongaeting.settings.base import *


PROFILE = 'Local'

DEBUG = True
CORS_ORIGIN_ALLOW_ALL = True

CORS_ORIGIN_WHITELIST = (
    'localhost:3000',
    '127.0.0.1:3000'
)
