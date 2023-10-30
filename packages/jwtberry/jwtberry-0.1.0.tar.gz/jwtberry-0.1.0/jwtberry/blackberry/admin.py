from django.contrib import admin

from .models import JwtBerry, BlackBerry


@admin.register(JwtBerry)
class JwtBerryAdmin(admin.ModelAdmin):
    list_display = (
        'jti',
        'user',
        'created_at',
        'expires_at',
    )

    search_fields = (
        'user__email',
        'user__id',
        'jti',
    )
    ordering = ('-created_at',)

    actions = None

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return request.method in ['GET', 'HEAD', 'OPTIONS'] or super().has_change_permission(request, obj)

    def get_readonly_fields(self, request, obj=None):
        return self.fields or [f.name for f in self.model._meta.fields]


@admin.register(BlackBerry)
class BlackBerryAdmin(admin.ModelAdmin):
    list_display = (
        'jti',
        'user',
        'created_at',
        'expires_at',
        'added_at',
    )
    search_fields = (
        'token__user__email',
        'token__user__id',
        'token__jti',
    )

    ordering = ('-added_at',)

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        return qs.select_related('token__user')

    @admin.display(description='User')
    def user(self, obj):
        return obj.token.user

    @admin.display(description='JTI')
    def jti(self, obj):
        return obj.token.jti

    @admin.display(description='Created At')
    def created_at(self, obj):
        return obj.token.created_at

    @admin.display(description='Expires At')
    def expires_at(self, obj):
        return obj.token.expires_at
