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
    'django.contrib.staticfiles',
    'debug_toolbar',
    'django_coverage',
    'ckeditor',
    'pagebits'
]

ROOT_URLCONF = 'pagebits.tests.urls'

SECRET_KEY = "herp-derp"

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware'
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
STATIC_ROOT = os.path.join(BASE_PATH, 'static_deploy')

TEMPLATE_DIRS = (
    os.path.join(BASE_PATH, 'templates'),
)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_PATH, 'media')

# Debug Toolbar
INTERNAL_IPS = ('127.0.0.1', )
DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.timer.TimerDebugPanel',
    'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
    'debug_toolbar.panels.headers.HeaderDebugPanel',
    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    'debug_toolbar.panels.template.TemplateDebugPanel',
    'debug_toolbar.panels.sql.SQLDebugPanel',
    'debug_toolbar.panels.signals.SignalDebugPanel',
    'debug_toolbar.panels.logger.LoggingPanel',
)

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
    'HIDE_DJANGO_SQL': False,
}

CKEDITOR_UPLOAD_PATH = '/tmp'
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'MyToolBar',
        'toolbar_MyToolBar': [[
            'Format', 'Bold', 'Italic', 'Outdent', 'Indent', 'NumberedList', 'BulletedList',
            'Link', 'Unlink', 'Anchor', 'Image', 'Source',
        ]],
        'removePlugins': 'elementspath, fonts',
        'forcePasteAsPlainText': True,
    },
}
