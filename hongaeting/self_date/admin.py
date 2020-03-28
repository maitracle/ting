from django.contrib import admin
from django.contrib.admin import register

from .models import Like, SelfDateProfile


@register(SelfDateProfile)
class SelfDateProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'profile',)


@register(Like)
class LikeAdmin(admin.ModelAdmin):
    pass
