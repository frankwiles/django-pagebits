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
