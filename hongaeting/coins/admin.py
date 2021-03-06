from django.contrib import admin
from django.contrib.admin import register

from coins.models import CoinHistory


@register(CoinHistory)
class SelfDateCoinHistoryAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'profile', 'rest_coin', 'reason', 'message', 'created_at', 'updated_at',
    )
    list_filter = ('reason', 'profile',)
    search_fields = ('profile',)
    ordering = ('-id',)
