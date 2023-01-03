from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.conf import settings
from .models import Event, User, Invitation
"""
admin.site.register(settings.AUTH_USER_MODEL, BaseUserAdmin)

admin.site.register(Event)
admin.site.register(User)
admin.site.register(Invitation)
"""