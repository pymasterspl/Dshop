from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    
    # default name
    # name = 'core'

    # New name, and label
    label='core'
    name = 'apps.core'