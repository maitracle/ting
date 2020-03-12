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


# media
DEFAULT_FILE_STORAGE = 'common.custom_storages.MediaStorage'

# MediaStorage

AWS_ACCESS_KEY_ID = os.environ['S3_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['S3_SECRET_ACCESS_KEY']

# s3 profile bucket
AWS_STORAGE_BUCKET_NAME = os.environ['AWS_STORAGE_BUCKET_NAME']

# Todo(maitracle): 아래 두 세팅값 필요한지?
# AWS_S3_HOST = 's3.ap-northeast-2.amazonaws.com'
# AWS_QUERYSTRING_AUTH = False

AWS_S3_REGION_NAME = 'ap-northeast-1'
AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com"

MEDIA_ROOT = 'media'
MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{MEDIA_ROOT}/"

AWS_IS_GZIPPED = True
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
