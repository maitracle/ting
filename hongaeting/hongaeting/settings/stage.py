import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from hongaeting.settings.base import *


PROFILE = 'Stage'

DEBUG = False


# sentry
sentry_sdk.init(
    dsn=os.environ['SENTRY_DSN'],
    integrations=[DjangoIntegration()],
    environment=ENVIRONMENT,
)


# media files
DEFAULT_FILE_STORAGE = 'common.custom_storages.MediaStorage'
