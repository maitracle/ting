from django.contrib import admin
from django.contrib.admin import register

from self_date.models import Like


@register(Like)
class LikeAdmin(admin.ModelAdmin):
    pass
