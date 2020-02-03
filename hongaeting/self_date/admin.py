from django.contrib import admin
from django.contrib.admin import register

from self_date.models import CoinHistory


@register(CoinHistory)
class SelfDateCoinHistoryAdmin(admin.ModelAdmin):
    pass