from django.db import models

from common.constants import COIN_CHANGE_REASON
from common.models import BaseModel


class CoinHistory(BaseModel):
    """
    포인트 사용내역에 대한 기록입니다.
    CoinHistory는 'users.Profile' 모델과 1:다 관계입니다.
    """
    profile = models.ForeignKey('users.Profile', related_name='coin_histories', on_delete=models.CASCADE,
                                null=True, blank=True, verbose_name='해당유저의 공통닉네임')

    rest_coin = models.PositiveSmallIntegerField(verbose_name='남은 포인트')
    reason = models.CharField(max_length=50, choices=COIN_CHANGE_REASON, verbose_name='포인트차감이유')
    message = models.CharField(max_length=200, verbose_name='포인트차감 메세지')
