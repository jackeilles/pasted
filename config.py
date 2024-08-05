import os

class Config:
    # This is the directory all files for pasted.sh will go under, choose wisely.
    # DO NOT ADD A TRAILING SLASH!!
    BASEDIR = '/home/jackeilles/pasted'

    # This is for CSRF protection, use either and make sure its completely random.
    # The key in here is a placeholder, DO NOT USE THIS IN PRODUCTION!
    SECRET_KEY = os.environ.get('SECRET_KEY') or '02e155772e3ff5942eac543691dd4dce1b424e825385f81f653303632e0b85ed'

    # Database URI, simple as that.
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or f'sqlite:///{BASEDIR}/pasted.db'

    # How large the content can be before it is rejected with a 413 Content Too Large.
    MAX_CONTENT_LENGTH = 256 * 1024 * 1024

    # How long a URL to shorten can be before its flat out rejected with a 414 (who's got urls at 2048 chars anyway???)
    MAX_URL_LEN = 2048

    # How long a file name can be before it is rejected with a 414 Request-URI Too Long
    MAX_FILE_NAME = 64

    # Min and Max time before a URL expires in milliseconds
    MIN_EXPIRE = 28 * 24 * 60 * 60 * 1000 # days first, everything else is hour, min, sec and calc
    MAX_EXPIRE = 365 * 24 * 60 * 60 * 1000

    # Which domains do we actually own? They're all listed here!
    VALID_SERVER_NAME = ["pasted.sh"]

    # Here is where we store all uploaded files.
    FILE_PATH = f'{BASEDIR}/files/'

    # Self-explanatory, no executables, no archives.
    # Returns a 415 Unsupported Media Type if the mimetype is in this list.
    DISALLOWED_MIME_TYPES = [
                            'application/x-dosexec',
                            'application/x-executable',
                            'application/x-sharedlib',
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
                            'application/vnd.debian.binary-package',
                            'application/x-rpm',
                            'application/x-msdownload',
                            'application/x-python-code',
                            'application/x-elf',
                            'application/x-msdos-program',
                            'application/vnd.microsoft.portable-executable',
                            'application/x-bat',
                            'application/x-sh',
                            'message/rfc822',
                            'application/x-mimearchive',
                            'application/vnd.ms-excel',
                            'application/vnd.ms-powerpoint',
                            'application/msword',
                            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                            'application/vnd.openxmlformats-officedocument.presentationml.presentation'
                            ]
