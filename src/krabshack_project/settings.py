import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = os.getenv('SECRET_KEY')


# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = int(os.getenv('DEBUG', default=0))

ALLOWED_HOSTS = [
    'web',
    'krabshack.space',
    'www.krabshack.space'
]
if DEBUG:
    ALLOWED_HOSTS += '*'


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social_django',
    'site_app.apps.SiteAppConfig',
    'tables_app.apps.TablesAppConfig',
    'esi_app.apps.EsiAppConfig',
    'data_app.apps.DataAppConfig',
    'fit_app.apps.FitAppConfig'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
]

ROOT_URLCONF = 'krabshack_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'krabshack_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB'),
        'HOST': os.getenv('DATABASE_URL'),
        'PORT': os.getenv('DATABASE_PORT'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD')
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

if DEBUG:
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, 'static'),
        '/static/',
    ]
else:
    STATIC_ROOT = '/static'

MEDIA_URL = '/media/'

MEDIA_ROOT = '/media'


# Authentication backends

AUTHENTICATION_BACKENDS = [
    'social_core.backends.eveonline.EVEOnlineOAuth2',
    'django.contrib.auth.backends.ModelBackend',
]


# Authentication settings

if DEBUG:
    SOCIAL_AUTH_EVEONLINE_KEY = os.getenv('SSO_CLIENT_DEVELOPMENT')
    SOCIAL_AUTH_EVEONLINE_SECRET = os.getenv('SSO_SECRET_DEVELOPMENT')
else:
    SOCIAL_AUTH_EVEONLINE_KEY = os.getenv('SSO_CLIENT_PRODUCTION')
    SOCIAL_AUTH_EVEONLINE_SECRET = os.getenv('SSO_SECRET_PRODUCTION')
SOCIAL_AUTH_CLEAN_USERNAMES = False
SOCIAL_AUTH_REDIRECT_IS_HTTPS = False
SESSION_COOKIE_SAMESITE = None

LOGIN_URL = 'login'
LOGOUT_URL = 'logout'
LOGIN_REDIRECT_URL = 'home'
LOGIN_ERROR_URL = 'home'


# Table settings

USE_THOUSAND_SEPARATOR = True


# ESI settings

ESI_TOKEN_KEY = os.getenv('ESI_TOKEN')  # random gibberish
ESI_DATASOURCE = 'tranquility'  # Change it to 'singularity' to use the test server
ESI_SWAGGER_JSON = f'https://esi.tech.ccp.is/latest/swagger.json?datasource={ESI_DATASOURCE}'
ESI_USER_AGENT = 'William Pierce EsiPy'  # for CCP to have contact info
ESI_CALLBACK =  f"{os.getenv('BASE_URL')}esi/callback"  # the callback URI you gave CCP
if DEBUG:
    ESI_SECRET_KEY = os.getenv('ESI_SECRET_DEVELOPMENT')  # your secret key
    ESI_CLIENT_ID = os.getenv('ESI_CLIENT_DEVELOPMENT')  # your client ID
else:
    ESI_SECRET_KEY = os.getenv('ESI_SECRET_PRODUCTION')  # your secret key
    ESI_CLIENT_ID = os.getenv('ESI_CLIENT_PRODUCTION')  # your client ID


# Security settings

if not DEBUG:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 3600
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_SSL_REDIRECT = False
    SECURE_REFERRER_POLICY = 'no-referrer'
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_PROXY_SSL_HEADER=('HTTP_X_FORWARDED_PROTO', 'https')
