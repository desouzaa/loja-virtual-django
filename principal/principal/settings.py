
from pathlib import Path
import django_on_heroku
import os
import environ



# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '7)fe57o6#0jgiwg_fc3nzp=0(#swrbbyo7eq21$x(1168gw(4+'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'pages',
    'users.apps.UsersConfig',
    'produtos',
    'pedidos',
    'payments',
    'outros',
    # 'anymail',
    
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'principal.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'pages')],
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

WSGI_APPLICATION = 'principal.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DB_NAME', 'bulldogstore'),
        'USER': os.environ.get('DB_USER', 'postgres'),
        'PASSWORD': os.environ.get('DB_PASS', 'rafa123'),
        'HOST': 'localhost',
        'PORT': '5432',
        
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

MEDIA_ROOT = (
  os.path.join(BASE_DIR, 'media') #pasta media para abrigar os arquivos dos usuários
)

MEDIA_URL = '/media/'

LOGIN_REDIRECT_URL = '/templates/pages/login'

LOGOUT_REDIRECT_URL = '/templates/pages/index'

AUTH_USER_MODEL = "users.User"

env = environ.Env()
env.read_env(str(BASE_DIR / ".env"))
MERCADO_PAGO_PUBLIC_KEY= env("MERCADO_PAGO_PUBLIC_KEY")
MERCADO_PAGO_ACCESS_TOKEN= env("MERCADO_PAGO_ACCESS_TOKEN")

# EMAIL_BACKEND = "anymail.backends.mailgun.EmailBackend"
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# DEFAULT_FROM_EMAIL = "no-reply@bulldog.com"
# SERVER_EMAIL = DEFAULT_FROM_EMAILanymail = {
#     "MAILGUN_API_KEY": "86146f01f3d9975a3c5b31dd11f49b9c-7b8c9ba8-90f058d7",
#     "MAILGUN_SENDER_DOMAIN": "sandbox598c1115c86a44859c7cfba4099a47ec.mailgun.org"
# }

django_on_heroku.settings(locals())