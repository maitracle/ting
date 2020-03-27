from django.contrib import admin
from django.contrib.admin import register

from coins.models import CoinHistory


@register(CoinHistory)
class SelfDateCoinHistoryAdmin(admin.ModelAdmin):
    pass
