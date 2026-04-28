from django.apps import AppConfig


class IncidentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'incidents'
    verbose_name = 'Gestion des incidents'

    def ready(self):
        from .compat import patch_django_template_context_copy

        patch_django_template_context_copy()
