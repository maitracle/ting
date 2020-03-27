from django.contrib import admin
from django.contrib.admin import register

from profiles.models import SelfDateProfile


@register(SelfDateProfile)
class SelfDateProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'profile',)
