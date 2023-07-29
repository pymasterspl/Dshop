from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'

    # default name
    # name = 'core'

    # New name, and label
    label = 'users'
    name = 'apps.users'
