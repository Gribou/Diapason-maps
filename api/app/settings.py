"""
Django settings for coconut project.

Generated by 'django-admin startproject' using Django 3.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv(
    "SECRET_KEY", 'django-insecure-b=-$pezt9085s21piek$5u4t319)lve^zw@4rbqclx%%9l3yir')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG", "False") == "True"

if DEBUG:
    ALLOWED_HOSTS = ['*']
    CORS_ORIGIN_ALLOW_ALL = True
else:
    ALLOWED_HOSTS = ['*']
    a_h_list = [a_h for a_h in os.getenv(
        "ALLOWED_HOSTS", '').replace('"', '').split(' ')] if os.getenv(
        "ALLOWED_HOSTS", None) else []
    # so that API can be usable by other websites, we allow cross-origin requests (when not authenticated)
    CORS_ORIGIN_ALLOW_ALL = True
    # CORS_ORIGIN_WHITELIST = ['https://{}'.format(a_h) for a_h in a_h_list]
    # CORS_ORIGIN_WHITELIST.append('http://localhost')
    CSRF_TRUSTED_ORIGINS = ['https://{}'.format(a_h) for a_h in a_h_list]
    CSRF_TRUSTED_ORIGINS.append('http://localhost')
    CSRF_COOKIE_HTTPONLY = False
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = True
    # indispensable pour servir des fichiers media avec le bon protocole :
    USE_X_FORWARDED_HOST = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Applications tierces
    'constance',
    'constance.backends.database',
    'rest_framework',
    'corsheaders',
    'django_celery_results',
    'django_celery_beat',
    'treenode',

    # Applications Coconut
    'scraper',
    'airfields',
    'civ',
    'acc',
    'phones',
    'files',
    'nav',
    'tiles',
    'radionav',
    'sso',
    'api',
]

SITE_ID = 1

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'sso.middleware.KeycloakMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

if DEBUG:
    MIDDLEWARE = [
        'debug_toolbar.middleware.DebugToolbarMiddleware'] + MIDDLEWARE
    INTERNAL_IPS = ['127.0.0.1']  # for debug toolbar
    INSTALLED_APPS += ['debug_toolbar', 'django_extensions']
else:
    MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates_web'),
                 os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': os.getenv("DB_ENGINE", 'django.db.backends.sqlite3'),
        'NAME': os.getenv("DB_NAME", os.path.join(BASE_DIR, 'db.sqlite3')),
        'USER': os.getenv("DB_USER", ''),
        'PASSWORD': os.getenv("DB_PASSWORD", ''),
        'HOST': os.getenv("DB_HOST", ''),
        'PORT': os.getenv("DB_PORT", '')
    }
}


AUTHENTICATION_BACKENDS = [
    'sso.authentication.KeycloakAuthorizationBackend',
    'django.contrib.auth.backends.ModelBackend'
]

LOGOUT_REDIRECT_URL = "admin:login"
LOGIN_REDIRECT_URL = "admin:index"

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = []


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'fr'

TIME_ZONE = 'Europe/Paris'

USE_I18N = True

USE_L10N = True

USE_TZ = True

DEFAULT_CHARSET = 'utf-8'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

URL_ROOT = os.getenv("URL_ROOT", '/')
FORCE_SCRIPT_NAME = CSRF_COOKIE_PATH = LANGUAGE_COOKIE_PATH = SESSION_COOKIE_PATH = URL_ROOT

# Fichiers statiques (CSS, JavaScript, Images)
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static_gen'),
    os.path.join(BASE_DIR, 'static_web'),
]
STATIC_URL = URL_ROOT + 'static/'
WHITENOISE_STATIC_PREFIX = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
if not DEBUG:
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Fichiers enregistrés
MEDIA_URL = URL_ROOT + 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

EMAIL_BACKEND = os.getenv("EMAIL_BACKEND", None)
if EMAIL_BACKEND:
    # Envoi de mail par serveur SMTP (internet DGAC)
    EMAIL_HOST = os.getenv("EMAIL_HOST", '')
    EMAIL_PORT = os.getenv("EMAIL_PORT", "")
    EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", '')
    EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")
    EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "False") == "True"
else:
    # mock email sending in "sent_emails" directory
    EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
    EMAIL_FILE_PATH = os.path.join(BASE_DIR, "sent_emails")

# use CONSTANCE_CONFIG instead
ADMINS = [('Admin', os.getenv('EMAIL_ADMIN', None))]
DEFAULT_FROM_EMAIL = os.getenv(
    "EMAIL_ADMIN", None)  # pour les autres emails
SERVER_EMAIL = DEFAULT_FROM_EMAIL  # pour les messages d'erreur

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

os.environ['SCRAPY_SETTINGS_MODULE'] = 'scraper.settings'

CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'
CONSTANCE_CONFIG = {
    'EMAIL_ADMIN': (os.getenv('EMAIL_ADMIN', "root@localhost"),
                    "Adresse e-mail de l'administrateur"),
    'EMAIL_SUBJECT_PREFIX':
    ('[COCONUTS] ',
     'Préfixe ajouté aux sujets des emails envoyés automatiquement'),
    'AIRAC_UPDATE_MANAGERS': ("", "Adresses e-mails à notifier lors d'une mise à jour automatique (séparées par des ;)"),
    'AIRAC_REF': ("2021-03-25", "Date d'un changement de cycle AIRAC de référence (les suivants sont calculés tous les 28 jours à partir de cette date)."),
    'RADIO_COVERAGE_ENABLED': (False, "Permettre la configuration de la couverture radio des fréquences"),
    'PHONES_ENABLED': (False, "Permettre la mise à disposition d'un annuaire téléphonique (cf 'Téléphones')"),
    'FALLBACK_URL': ("", "URL d'une autre instance de Diapason-Coconuts permettant de récupérer les données si les AIP sont inaccessibles (ex : https://dev.diapason.kalif.asap.dsna.fr/coconuts/)"),
    'FILES_ENABLED': (False, "Permettre l'import de fichiers PDF autres"),
    'KEYCLOAK_ENABLED': (False, "Utiliser l'authentification SSO avec un serveur Keycloak"),
    'KEYCLOAK_SERVER_URL': ("http://localhost:8080/auth/", "URL du serveur Keycloak"),
    'KEYCLOAK_REALM': ('diapason', 'Nom de royaume Keycloak'),
    'KEYCLOAK_CLIENT_ID': ("diapason", 'Identifiant de client Keycloak de cette application'),
    'KEYCLOAK_CLIENT_SECRET': ("__secret__", "Secret de client Keycloak de cette application"),
}
CONSTANCE_CONFIG_FIELDSETS = {
    "Envoi d'emails":
    ('EMAIL_ADMIN', 'EMAIL_SUBJECT_PREFIX'),
    "Mise à jour AIRAC": ("AIRAC_REF", 'AIRAC_UPDATE_MANAGERS', 'FALLBACK_URL'),
    "Fonctionnalités": ("PHONES_ENABLED", "RADIO_COVERAGE_ENABLED", 'FILES_ENABLED'),
    "SSO Keycloak": ("KEYCLOAK_ENABLED", "KEYCLOAK_SERVER_URL", "KEYCLOAK_REALM", "KEYCLOAK_CLIENT_ID", 'KEYCLOAK_CLIENT_SECRET'),
}

REST_FRAMEWORK = {
    'DEFAULT_VERSIONING_CLASS':
        'rest_framework.versioning.AcceptHeaderVersioning',
    'DEFAULT_VERSION': '1.0',
    'ALLOWED_VERSIONS': ['1.0'],
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    'PAGE_SIZE': 30,
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication'
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
}

CELERY_TIMEZONE = TIME_ZONE
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", None)
CELERY_TASK_DEFAULT_QUEUE = os.getenv("CELERY_QUEUE", "coconuts")
CELERY_RESULT_BACKEND = 'django-db'
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"
# prevent scrapy error "ReactorNotRestartable"
CELERY_WORKER_MAX_TASKS_PER_CHILD = 1
# do not send task to queue if no broker, run task locally (blocking) :
CELERY_TASK_ALWAYS_EAGER = CELERY_BROKER_URL is None

SILENCED_SYSTEM_CHECKS = [
    "rest_framework.W001",  # no default pagination class
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
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
            'class': 'api.email.ConstanceAdminEmailHandler'
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        '': {
            'handlers': ["console"],
            "level": "DEBUG",
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.security': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        }
    }
}

try:
    from app.version import __version__
    VERSION_TAG = __version__
except:
    VERSION_TAG = "?"
