# Django settings for project.
import os.path

ROOT_DIR = os.path.dirname(__file__)

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
     ('Brian Thorne', 'hardbyte@gmail.com'),
)

ALLOWED_HOSTS = ['.hardbyte.webfactional.com']

TWITTER_CONSUMER_KEY         = ''
TWITTER_CONSUMER_SECRET      = ''

GOOGLE_CONSUMER_KEY          = ''
GOOGLE_CONSUMER_SECRET       = ''
GOOGLE_OAUTH2_CLIENT_ID      = ''
GOOGLE_OAUTH2_CLIENT_SECRET  = ''

FACEBOOK_APP_ID = "386541278102635"
FACEBOOK_API_SECRET = "08fd5dddc6329c7c56ce980e07a5d83d"
SOCIAL_AUTH_FORCE_POST_DISCONNECT = True

LASTFM_API_KEY = '2f42e9b46522dc31c099904e3a94f6b1'
LASTFM_SECRET = 'f17d10f5aaf23a34e270370e6d030c6c'

# NOTE: to get users email addresses, you must request the email permission
FACEBOOK_EXTENDED_PERMISSIONS = [
    'user_actions.music',
    'user_location',
    #'friends_actions.music'
]
APPEND_SLASH = False
MANAGERS = ADMINS

# http://django-social-auth.readthedocs.org/
AUTHENTICATION_BACKENDS = (
    #'social_auth.backends.twitter.TwitterBackend',
    'social_auth.backends.facebook.FacebookBackend',
    #'social_auth.backends.google.GoogleOAuthBackend',
    'social_auth.backends.google.GoogleOAuth2Backend',
    #'social_auth.backends.google.GoogleBackend',
    #'social_auth.backends.yahoo.YahooBackend',
    #'social_auth.backends.browserid.BrowserIDBackend',
    #'social_auth.backends.OpenIDBackend',
    'django.contrib.auth.backends.ModelBackend',
    )


EMAIL_HOST = 'smtp.webfaction.com'
EMAIL_HOST_USER = 'mailbox_username'
EMAIL_HOST_PASSWORD = 'mailbox_password'
DEFAULT_FROM_EMAIL = 'valid_email_address'
SERVER_EMAIL = 'valid_email_address'

SOCIAL_AUTH_DEFAULT_USERNAME = 'new_social_auth_user'

DATABASES = {
    'default': {
        # maybe we can map straight to google app engine?
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'partysense',                      # Or path to database file if using sqlite3.
        'USER': 'partysense',                      # Not used with sqlite3.
        'PASSWORD': 'fV#BXd!aKPNAL0h',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'NZ'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# eg DJ's photo?
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = '/home/hardbyte/webapps/media_partysense/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = 'http://partysense.hardbyte.webfactional.com/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = '/home/hardbyte/webapps/static_partysense/'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = 'http://partysense.hardbyte.webfactional.com/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(ROOT_DIR, os.path.pardir, 'partysense', 'static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'sfx8+pzj%xni=rp5iu@v!r)uly%5a+=rat*52mj0$#ite9_9lv'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.request',
    #'django.core.context_processors.i18n',
    #'django.core.context_processors.media',
    #'django.contrib.messages.context_processors.messages',

    'social_auth.context_processors.social_auth_by_type_backends',
    # Adds a social_auth dict where each key is a provider name and its value is a UserSocialAuth instance if user
    # has associated an account with that provider, otherwise None
    #'social_auth.context_processors.social_auth_by_name_backends',
    )

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',

    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'partysense.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'partysense.wsgi.application'


TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(ROOT_DIR, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    # enable the admin and admin documentation:
    'django.contrib.admin',
    'django.contrib.admindocs',

    # for database migrations http://south.readthedocs.org
    #'south',

    # for authentication with facebook etc
    'social_auth',

    # our core application
    'partysense.event',
    'partysense.music',
    'partysense.dj'

)

LOGIN_URL          = '/profile/'
LOGIN_REDIRECT_URL = '/profile/'
LOGIN_ERROR_URL    = '/profile/login/'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            #'formatter': 'simple'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        '': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
        }
    }
}

try:
    from local_settings import *
except ImportError:
    pass