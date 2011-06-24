# Django settings for iflatshare project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Muhammad Rahman', 's@s.com'),
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'mysql'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'sewinzco_iflatshare_qa'             # Or path to database file if using sqlite3.
DATABASE_USER = 'sewinzco'             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = 'localhost'             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/London'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-GB'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = '/home2/sewinzco/www/iflatshare/qa/iflatshare/media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/site_media/admin/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '4j002-zj8x5*ikq%l_-e-igb33q6-+)qttwio-a+2u8zcz_c%4'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
)

ROOT_URLCONF = 'iflatshare.urls'

#SERIALIZATION_MODULES = {
#        'yml': "django.core.serializers.pyyaml"
#} 

TEMPLATE_DIRS = (
    "/home2/sewinzco/www/iflatshare/qa/iflatshare/templates",
    "/home2/sewinzco/www/iflatshare/qa/iflatshare/core/templates"
)

ENV = 'QA'
VERSION = '1.5.0'
COMMIT = {'hash': 'cc8a696',
          'url': '''https://github.com/mrahma01/iflatshare'''\
                 '''/commit/cc8a696dbcbcc1f5985f19613dede7895c2f3699'''}

HONEYPOT_FIELD_NAME = 'contact'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_HOST_USER = 'localhost'
EMAIL_HOST_PASSWORD = ''
DEFAULT_FROM_EMAIL = 'admin@iflatshare'
DEFAULT_TO_EMAIL = 'mmrs151@gmail.com'
EMAIL_PORT = 25

CCOUNT_ACTIVATION_DAYS = 2

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.humanize',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'iflatshare.core',
    'envelope',
    'honeypot',
    'registration',
    'south',
)

ACCOUNT_INVITATION_DAYS = 10
INVITATIONS_PER_USER = 10
AUTH_PROFILE_MODULE = 'core.Profile'

LOGIN_REDIRECT_URL = '/avg_diff/'

INVITE_MODE = True
