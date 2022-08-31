# 本番環境
from .development import *

# env
DEBUG = False

ALLOWED_HOSTS = ["*", ]

# AWS settings
AWS_ACCESS_KEY_ID = 'AKIA3WIDXO7BR2GOJ6V6'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'developeer-storage'

AWS_LOCATION = 'media'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

S3_URL = 'http://%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME

# DB settings
DATABASES = {
    'default': env.db()
}
