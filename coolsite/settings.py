from pathlib import Path
import environ

BASE_DIR = Path(__file__).resolve().parent.parent

# Here we read the .env file
env = environ.Env()
env.read_env(BASE_DIR / '.env')

REQUIRED_CAPTCHA = env.bool('REQUIRED_CAPTCHA', default=True)

DEBUG = env('DEBUG')

SECRET_KEY = env('SECRET_KEY')

# ALLOWED_HOSTS = env('HOST_1'), env('HOST_2'), env('LOCAL_HOST')
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')

NON_LOCAL_APPS = [
    'captcha',
    'debug_toolbar',
    'women.apps.WomenConfig',
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
] + NON_LOCAL_APPS

CAPTCHA_BACKGROUND_COLOR = '#f9d1ff'
CAPTCHA_IMAGE_SIZE = (150, 40)
CAPTCHA_LENGTH = 4

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'coolsite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # пишем путь для того чтобы переназначить стандарные шаблоны,
        # взяв название файла base_site.html из папки venv, создадим файл с таким же названием в templates, но
        # уже с кастомным содержимым, для того чтобы иметь возмож. настроить панель под себя. Это работает
        # т.к джаного сначала ищет кастомные шаблоны для отображения страницы, а в случае их отсутствия,
        # использует стандартные из venv.
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

WSGI_APPLICATION = 'coolsite.wsgi.application'

DATABASES = { 
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
# Для локальной машины

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': "wenturum_django",
#         'USER': 'wenturum_django',
#         "PASSWORD": 'qNXuuZgR1_12',
#         'HOST': 'localhost',
#         'PORT': '3306',
#     }
# }

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

LANGUAGE_CODE = 'en'  # en-us

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'static'
STATICFILES_DIRS = []


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_ROOT = BASE_DIR / 'media/'
MEDIA_URL = '/media/'

# LOGIN_REDIRECT_URL = '/'

INTERNAL_IPS = [
    "127.0.0.1",
]

""" Кэширование. Тут задается место, в котором будет содержаться сохраненный кэш. """
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': BASE_DIR / 'coolsite_cache',
    }
}

""" Для кэширования, в корневой папке проекта(coolsite) нужно создать папку с названием "coolsite_cache".
Можно кэшировать данные на уровне шаблонов(в файлах .html), с пом. API низкого уровня(в views.py или utils.py), и на 
уровне представлений(в urls.py).
Для кэширования на уровне представлений нужно в урлах прописать: 

urlpatterns = [
    path('', cache_page(60)(WomenHome.as_view()), name='home'),
    ] 
"""
