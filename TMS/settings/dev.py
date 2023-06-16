from .common import *

SECRET_KEY = 'django-insecure-ki2j_&zb!dq%0d90ezdj^b(b57qsmpp40+oomc97dxo+4s63l-'

ALLOWED_HOSTS = ['*']
DEBUG = True

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'afaker',
#         'HOST': 'localhost',
#         'USER': 'root',
#         'PASSWORD': 'Ahmed@123',
#     }
# }

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = { 
    'default':  parse(env('DATABASE_URL')) 
}

CSRF_TRUSTED_ORIGINS = [
    'http://127.0.0.1',
    'https://tms-wf.netlify.app/',
]