# Django settings for SocialMediaHarvester project.
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP
import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
     ('Tobias Wetzel', 'tobias.wetzel@iao.fraunhofer.de'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'smh',                      # Or path to database file if using sqlite3.
        'USER': 'postgres',                      # Not used with sqlite3.
        'PASSWORD': 'h7G2Ssf92thVl',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '5432'                      # Set to empty string for default. Not used with sqlite3.
    },
    'mongoDB':{
        'HOST': 'localhost',
        'PORT': 27017
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'UTC'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = False

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = 'C:/djangoFileFolder/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = 'http://127.0.0.1:8000/media/'

ADMIN_MEDIA_PREFIX = '/static/admin/'

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_URL = 'http://127.0.0.1:8080'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PROJECT_DIR, 'static')

#log files
LOG_DIR = os.path.join(PROJECT_DIR, 'logs')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = PROJECT_URL + '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)


#path to the Harvester-Folder
#PATH_TO_HARVESTERS = STATIC_ROOT+"\\Harvesters\\"
PATH_TO_HARVESTERS = os.path.join(PROJECT_DIR,'modules')

#path to the file which contains the list of installed harvesters
#PATH_TO_INSTALLED_HARVESTERS_TXT = PATH_TO_HARVESTERS+"installedHarvesters.txt"
PATH_TO_INSTALLED_HARVESTERS_INI = PATH_TO_HARVESTERS+"/installedModules.ini"

#Framework Parameters
PATH_TO_GLOBAL_PARAMTERS_JSON = PATH_TO_HARVESTERS+'/global_parameters.json'

#Framework META Parameters
PATH_TO_META_PARAMTERS_JSON = PATH_TO_HARVESTERS+"/meta_parameters.json"

# Make this unique, and don't share it with anybody.
SECRET_KEY = '-1gs3#p1=%h(-(8d@jfx@#pdn-gv1acv6etw8d=7vtpo+tss2k'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    'django.core.context_processors.request',
)


AUTH_PROFILE_MODULE = 'django.contrib.auth.models.User'



MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'SocialMediaHarvester.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'SocialMediaHarvester.wsgi.application'

TEMPLATE_DIRS = ('/var/www/smh/html/SocialMediaHarvester/SocialMediaHarvester/templates'
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)


INSTALLED_APPS = (
    'kombu.transport.django',            
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    #'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'SocialMediaHarvester.database',
    # Uncomment the next line to enable the admin:
     'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
     'django.contrib.admindocs',
)


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
    },
    'formatters': {
        'standard': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
       },
        'logfile': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': LOG_DIR + "/logfile.log",
            'maxBytes': 50000,
            'backupCount': 2,
            'formatter': 'standard',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'smh': {
            'handlers': ['logfile'],
            'level': 'DEBUG',
        },
    }
}
