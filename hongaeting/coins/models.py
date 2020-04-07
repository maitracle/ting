from django.db import models

from common.constants import COIN_CHANGE_REASON
from common.models import BaseModel


class CoinHistory(BaseModel):

    profile = models.ForeignKey('users.Profile', related_name='coin_histories', on_delete=models.CASCADE, null=True, blank=True)

    rest_coin = models.PositiveSmallIntegerField()
    reason = models.CharField(max_length=50, choices=COIN_CHANGE_REASON)
    message = models.CharField(max_length=200)
