from django.contrib import admin
from django.contrib.admin import register

from users.models import User


@register(User)
class UserAdmin(admin.ModelAdmin):
    pass
