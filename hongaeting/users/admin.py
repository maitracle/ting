from django.contrib import admin
from django.contrib.admin import register

from users.models import User


@register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'email', 'university_email', 'is_confirmed_student', 'user_code', 'is_staff', 'is_superuser', 'is_active')
