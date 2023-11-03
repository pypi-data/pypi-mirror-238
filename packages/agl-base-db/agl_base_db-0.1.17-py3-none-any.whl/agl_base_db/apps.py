from django.apps import AppConfig


class AglBaseDbConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'agl_base_db'
    verbose_name = "AGL Base Database"
