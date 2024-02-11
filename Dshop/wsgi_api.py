import os

try:  # prevents sorting with isort
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Dshop.settings")

    from django.core.wsgi import get_wsgi_application
except KeyboardInterrupt:
    pass

application = get_wsgi_application()
