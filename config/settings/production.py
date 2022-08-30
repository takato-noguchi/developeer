# 本番環境
from .development import *

# env
DEBUG = False

ALLOWED_HOSTS = ["*", ]

# AWS settings
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME')
AWS_S3_SIGNATURE_VERSION = os.environ.get('AWS_S3_SIGNATURE_VERSION')

AWS_LOCATION = 'media'
# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media_root')

S3_URL = 'http://%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
MEDIA_URL = S3_URL

# DB settings
DATABASES = {
    'default': env.db()
}
