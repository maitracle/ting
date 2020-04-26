from django.contrib import admin
from django.contrib.admin import register

from .models import SelfDateLike, SelfDateProfile


@register(SelfDateProfile)
class SelfDateProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'profile', 'nickname', 'height', 'body_type', 'religion', 'is_smoke', 'image', 'chat_link',)
    list_display_links = ('id', 'profile', 'nickname')
    search_fields = ('nickname', )
    ordering = ('-id', )

    fieldsets = (
        ('기본정보', {
            'fields': ('profile', 'is_active', 'nickname', 'height', 'body_type', 'religion', 'is_smoke',)
        }),
        ('리스트정보', {
            'fields': ('tags', 'image', 'one_sentence')
        }),
        ('서술형정보', {
            'fields': ('appearance', 'personality', 'hobby', 'date_style', 'ideal_type',)
        }),
        ('채팅링크', {
            'fields': ('chat_link',)
        })
    )


@register(SelfDateLike)
class SelfDateLikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'self_date_profile', 'liked_self_date_profile')
    list_display_links = ('id',)
    ordering = ('-id',)