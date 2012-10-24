import os

BASE_PATH = os.path.dirname(__file__)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'pagebits',
    }
}

SITE_ID = 1

DEBUG = True

#TEST_RUNNER = 'django_coverage.coverage_runner.CoverageRunner'

#COVERAGE_MODULE_EXCLUDES = [
#    'tests$', 'settings$', 'urls$',
#    'common.views.test', '__init__', 'django',
#    'migrations', 'djcelery'
#]
#
#COVERAGE_REPORT_HTML_OUTPUT_DIR = os.path.join(BASE_PATH, 'coverage')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'pagebits'
]

ROOT_URLCONF = 'pagebits.tests.urls'

SECRET_KEY = "herp-derp"

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
)

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_PATH, 'static'),
)
