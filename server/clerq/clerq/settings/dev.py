from .base import *


DEBUG = True

INSTALLED_APPS += [
    "debug_toolbar",
]

# Middlewares
MIDDLEWARE.insert(4, "debug_toolbar.middleware.DebugToolbarMiddleware")

# Debug Toolbar
INTERNAL_IPS = ["127.0.0.1", "localhost"]
