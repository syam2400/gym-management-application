from django.contrib import admin
from .models import CustomUser


from django.contrib import admin
from django.contrib.sessions.models import Session
from django.utils.safestring import mark_safe
from django.contrib.sessions.backends.db import SessionStore

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_approved')
    list_filter = ('is_approved',)
    actions = ['approve_users']

    def approve_users(self, request, queryset):
        queryset.update(is_approved=True)

admin.site.register(CustomUser,CustomUserAdmin)





class SessionAdmin(admin.ModelAdmin):
    list_display = ['session_key', 'session_data', 'get_user', 'expire_date']
    readonly_fields = ['session_data_pretty']

    def get_user(self, obj):
        session_data = obj.get_decoded()
        uid = session_data.get('_auth_user_id')
        User = admin.site._registry.get(obj.get_decoded().get('_auth_user_backend', None))
        if User is not None:
            user = CustomUser.objects.get(pk=uid)
            return user.username
        return None
    get_user.short_description = 'User'

    def session_data_pretty(self, obj):
        return mark_safe('<pre>' + str(obj.get_decoded()) + '</pre>')
    session_data_pretty.short_description = 'Session Data'

    def has_add_permission(self, request):
        return False

admin.site.register(Session, SessionAdmin)
