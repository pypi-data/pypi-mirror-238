from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class JwtTokenConfig(AppConfig):
    name = "jwtberry.blackberry"
    verbose_name = _("JWT Token")
    default_auto_field = "django.db.models.BigAutoField"
