from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class JwtBerry(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    jti = models.CharField(unique=True, max_length=255)
    refresh_token = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    class Meta:
        db_table = 'jwtberries'

        abstract = ('jwtberry.blackberry' not in settings.INSTALLED_APPS)

        verbose_name = _('Jwtberry')
        verbose_name_plural = _('Jwtberries')

    def __str__(self):
        return f'Token for {self.user} - ({self.jti})'


class BlackBerry(models.Model):
    token = models.OneToOneField(
        JwtBerry,
        on_delete=models.CASCADE
    )

    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'blackberries'

        abstract = ('jwtberry.blackberry' not in settings.INSTALLED_APPS)

        verbose_name = _('Blackberry')
        verbose_name_plural = _('Blackberries')
