from django.db import models

from common.constants import COIN_CHANGE_REASON
from common.models import BaseModel


class CoinHistory(BaseModel):
    profile = models.ForeignKey('users.Profile', related_name='coin_histories', on_delete=models.CASCADE,
                                null=True, blank=True, verbose_name='해당유저의 프로필')

    rest_coin = models.PositiveSmallIntegerField(verbose_name='남은 포인트')
    reason = models.CharField(max_length=50, choices=COIN_CHANGE_REASON, verbose_name='포인트증감 이유')
    message = models.CharField(max_length=200, verbose_name='포인트증감 메세지')
