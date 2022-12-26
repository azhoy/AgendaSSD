from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Event, Member, EventParticipant, User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    pass


admin.site.register(Event)
admin.site.register(Member)
admin.site.register(EventParticipant)
