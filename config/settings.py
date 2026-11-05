import os
from pathlib import Path
import environ
from django.templatetags.static import static

# 1. Project Directory
BASE_DIR = Path(__file__).resolve().parent.parent

# 2. Initialize Environ
env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# 3. Secure Core Settings (Fetching from .env)
SECRET_KEY = env('SECRET_KEY')
DEBUG = env('DEBUG')
ALLOWED_HOSTS = ['*']

# 4. OpenAPI Docs Settings
SPECTACULAR_SETTINGS = {
    'TITLE': 'TaskForge API',
    'DESCRIPTION': 'Backend API for the TaskForge project management system.',
    'VERSION': '1.0.0',
}

INSTALLED_APPS = [
    'unfold',  # Added for Django Unfold Theme
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',  # OAUTH STEP: Required for allauth
    
    'rest_framework',   
    'rest_framework.authtoken', # OAUTH STEP: Required for dj-rest-auth
    'rest_framework_simplejwt',
    'rest_framework_api_key',
    
    # OAUTH STEP: allauth and dj-rest-auth apps
    'dj_rest_auth',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google', # Google OAuth Provider
    
    'django_filters',
    'drf_spectacular',
    'tasks.apps.TasksConfig',
]

# OAUTH STEP: Site ID is required by django.contrib.sites
SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware', # OAUTH STEP: allauth middleware
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'config.wsgi.application'

# PostgreSQL Database Connection
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'taskforge_db',       
        'USER': 'postgres',           
        'PASSWORD': 'Fai123$0',  
        'HOST': 'localhost',
        'PORT': '5432',
        'TEST': {
            'NAME': 'taskforge_fresh_test_db',  
        },
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Karachi'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

from datetime import timedelta

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 5,  
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=2),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'AUTH_HEADER_TYPES': ('Bearer',),
}

AUTH_USER_MODEL = 'tasks.CustomUser'

# OAUTH STEP: Authentication Backends
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# OAUTH STEP: dj-rest-auth JWT Configuration
REST_AUTH = {
    'USE_JWT': True,
    'JWT_AUTH_COOKIE': 'taskforge-auth',
    'JWT_AUTH_REFRESH_COOKIE': 'taskforge-refresh-token',
}
# OAUTH STEP: allauth Basic Settings (Email based login)
ACCOUNT_LOGIN_METHODS = {'email'}
ACCOUNT_SIGNUP_FIELDS = ['email*', 'password1*', 'password2*']
ACCOUNT_EMAIL_VERIFICATION = 'none'
# ==========================================
# LOGGING CONFIGURATION
# ==========================================
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'WARNING',  
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'debug.log',  
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'WARNING',
            'propagate': True,
        },
    },
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",  
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

#SESSION_ENGINE = "django.contrib.sessions.backends.cache"
#SESSION_CACHE_ALIAS = "default"

# CELERY SETTINGS (Redis Broker)
CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'

# TESTING EMAIL BACKEND (Console par email print karega)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# ==========================================
# Django Unfold Professional Configuration
# ==========================================

UNFOLD = {
    "SITE_TITLE": "TaskForge Admin",
    "SITE_HEADER": "TaskForge Dashboard",
    "SITE_URL": "/admin/",
    
    # STYLES list [] mein hai
    "STYLES": [
        lambda request: static("css/admin_custom.css"),
    ],

    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": False,
        "navigation": [
            {
                "title": "Task Management",
                "separator": True,
                "items": [
                    {
                        "title": "Workspaces",
                        "icon": "apartment",
                        "link": "/admin/tasks/workspace/",
                    },
                    {
                        "title": "Projects",
                        "icon": "folder",
                        "link": "/admin/tasks/project/",
                    },
                    {
                        "title": "Tasks",
                        "icon": "task",
                        "link": "/admin/tasks/task/",
                    },
                    {
                        "title": "Task Comments",
                        "icon": "comment",
                        "link": "/admin/tasks/taskcomment/",
                    },
                    {
                        "title": "Users",
                        "icon": "person",
                        "link": "/admin/tasks/customuser/",
                    },
                ],
            },
        ],
    },
}