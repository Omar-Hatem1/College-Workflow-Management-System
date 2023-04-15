from settings.common import *

SECRET_KEY = 'django-insecure-ki2j_&zb!dq%0d90ezdj^b(b57qsmpp40+oomc97dxo+4s63l-'


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

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
