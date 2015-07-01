"""
Django settings for e_shop project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '7rar^1x5r1wj3b1szuo($*5tf1f-u@(=@)0(#cu$i(h65lk(*p'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

TEMPLATE_LOADERS = (
                    'django_jinja.loaders.FileSystemLoader',
                    'django_jinja.loaders.AppLoader')
DEFAULT_JINJA2_TEMPLATE_EXTENSION = '.jinja'
JINJA2_EXTENSIONS = [
                    # The default extensions, you should include them
                    # if you are overwritting the settings.
                    "jinja2.ext.do",
                    "jinja2.ext.loopcontrols",
                    "jinja2.ext.with_",
                    "jinja2.ext.i18n",
                    "jinja2.ext.autoescape",
                    "django_jinja.builtins.extensions.CsrfExtension",
                    "django_jinja.builtins.extensions.CacheExtension",
                    "django_jinja.builtins.extensions.TimezoneExtension",
                    "django_jinja.builtins.extensions.UrlsExtension",
                    #"django_jinja.builtins.extensions.StaticFilesExtension",
                    "django_jinja.builtins.extensions.DjangoFiltersExtension",
                    'e_shop.extensions.StaticFileVersioningExtension'
                    ]

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_jinja',
    'sorl.thumbnail',
    'corsheaders',
    'oauth2_provider',
    'e_shop'
)
AUTHENTICATION_BACKENDS = (
    'oauth2_provider.backends.OAuth2Backend',
    # Uncomment following if you want to access the admin
    'django.contrib.auth.backends.ModelBackend'
                           )
MIDDLEWARE_CLASSES = (
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'oauth2_provider.middleware.OAuth2TokenMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'e_shop.middlewares.SessionManagerMiddleware'
)

ROOT_URLCONF = 'e_shop.urls'

WSGI_APPLICATION = 'e_shop.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'NAME':'e_shop',
        'ENGINE':'django.db.backends.mysql',
        'USER':'root',
        'PASSWORD':'root101'
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

MEDIA_ROOT = '/home/tristan/workplace/workspace_python/e_shop/src/e_shop/upload/'

MEDIA_URL = '/api/file/'

LOGIN_URL = '/account/login/'

CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = ('localhost:8000')