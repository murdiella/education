import os

ENVIRONMENT = os.environ.get('DJANGO_ENVIRONMENT', 'prod').lower()
if ENVIRONMENT == 'development':
    from .development import *
elif ENVIRONMENT == 'test':
    from .test import *
else:
    from .production import *
