from django.contrib import admin
from django.contrib.admin import register

from .models import SelfDateLike, SelfDateProfile


@register(SelfDateProfile)
class SelfDateProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'profile',)


@register(SelfDateLike)
class LikeAdmin(admin.ModelAdmin):
    pass
