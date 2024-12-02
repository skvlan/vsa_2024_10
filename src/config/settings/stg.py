from config.settings.base import *  # NOQA:

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-4u&^xsbn*af9(yqdljloxe+ci61!)!o(xs2xt&z-ggsyvkwuxb"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = []

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",  # NOQA:
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"
