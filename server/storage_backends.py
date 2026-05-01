from storages.backends.s3 import S3Storage

class StaticStorage(S3Storage):
    location = 'static'
    default_acl = None

class MediaStorage(S3Storage):
    location = 'media'
    default_acl = None
    file_overwrite = False