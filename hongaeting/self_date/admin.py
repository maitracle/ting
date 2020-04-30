from django.contrib import admin
from django.contrib.admin import register

from .models import SelfDateLike, SelfDateProfile


@register(SelfDateProfile)
class SelfDateProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'profile', 'nickname', 'height', 'body_type', 'religion', 'is_smoke', 'image', 'chat_link',)
    list_display_links = ('id', 'profile', 'nickname',)
    search_fields = ('nickname',)
    ordering = ('-id',)
    fields = (
        'profile', 'is_active', 'nickname', 'height', 'body_type', 'religion', 'is_smoke', 'tags', 'image',
        'one_sentence', 'appearance', 'personality', 'hobby', 'date_style', 'ideal_type', 'chat_link',
    )


@register(SelfDateLike)
class SelfDateLikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'self_date_profile', 'liked_self_date_profile',)
    list_display_links = ('id',)
    ordering = ('-id',)
