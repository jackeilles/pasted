import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'set-this-if-you-cant-use-env-vars'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'
    DISALLOWED_MIME_TYPES = ['application/x-dosexec', 
                            'application/x-executable', 
                            'application/x-sharedlib', 
                            'application/x-hdf5', 
                            'application/java-archive', 
                            'application/vnd.android.package-archive', 
                            'application/x-rar',
                            'application/zip',
                            'application/gzip',
                            'application/x-rar-compressed',
                            'application/vnd.rar',
                            'application/x-7z-compressed',
                            'application/x-tar',
                            'application/x-gtar',
                            'application/x-bzip-compressed-tar',
                            'application/x-gzip-compressed-tar',
                            'application/x-xz-compressed-tar',
                            'application/x-bzip',
                            'application/x-bzip2',
                            'application/x-xz',
                            'application/vnd.ms-cab-compressed',
                            'application/x-compress',
                            'application/x-compressed',
                            'application/x-lzh-compressed',
                            'application/x-arj',
                            'application/x-apple-diskimage',
                            'application/x-iso9660-image',
                            'application/x-stuffit',
                            'application/x-stuffitx',
                            'application/x-lha',
                            'application/x-cpio',
                            'application/vnd.debian.binary-package',
                            'application/x-rpm'
                            ] # These are MIME types that will be blocked on upload.
    