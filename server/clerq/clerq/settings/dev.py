from .base import *


DEBUG = True

INSTALLED_APPS += [
    "debug_toolbar",
]

# Static / Media
STATICFILES_DIRS += [
    BASE_DIR / "node_tools" / "node_modules",
]
MEDIA_ROOT = BASE_DIR / "mediafiles"

# Middlewares
MIDDLEWARE.insert(4, "debug_toolbar.middleware.DebugToolbarMiddleware")

# Debug Toolbar
INTERNAL_IPS = ["127.0.0.1", "localhost"]
