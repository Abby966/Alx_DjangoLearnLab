"""
Django settings for social_media_api project.
Django 5.2.4
"""

from pathlib import Path
import os  # <-- added
from datetime import timedelta  # (handy later if you switch to JWT)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------- Security / Env ----------------
# ❗ Replace hardcoded secrets in production. For now this keeps dev simple.
SECRET_KEY = os.getenv(
    "DJANGO_SECRET_KEY",
    "django-insecure-u^#1ss+oo8mm5k#sj=n2=uc7t=)tl-)8c4x9!q7=w6=070@d(p"  # <-- keep only for local dev
)

DEBUG = os.getenv("DJANGO_DEBUG", "1") == "1"  # <-- was True
ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "*").split(",")  # <-- was []

# ---------------- Apps ----------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party
    'rest_framework',
    'rest_framework.authtoken',

    # Local
    'accounts',
]

# ---------------- Middleware ----------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'social_media_api.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],  # <-- optional, useful later
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'social_media_api.wsgi.application'

# ---------------- Database ----------------
# Keep sqlite for now; swap to Postgres via env when deploying.
DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': os.getenv('DB_NAME', BASE_DIR / 'db.sqlite3'),
        # For Postgres you’d also set: USER, PASSWORD, HOST, PORT
    }
}

# ---------------- Password validation ----------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ---------------- I18N / TZ ----------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = os.getenv("TZ", "Africa/Nairobi")  # <-- was UTC
USE_I18N = True
USE_TZ = True

# ---------------- Static & Media ----------------
# Static (served by Django only in dev)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'  # <-- added for collectstatic in prod
STATICFILES_DIRS = [BASE_DIR / 'static'] if (BASE_DIR / 'static').exists() else []

# Media (for profile pictures/uploads)
MEDIA_URL = '/media/'          # <-- added
MEDIA_ROOT = BASE_DIR / 'media'  # <-- added

# ---------------- Primary key type ----------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ---------------- Auth / DRF ----------------
AUTH_USER_MODEL = 'accounts.User'

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
        # "rest_framework_simplejwt.authentication.JWTAuthentication",  # enable later if you prefer JWT
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}
