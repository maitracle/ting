from django.db import models
from model_utils import Choices

from common.models import BaseModel


class CoinHistory(BaseModel):
    CHANGE_REASON = Choices('CONFIRM_USER', 'SELF_DATE_PROFILE_VIEW', 'SELF_DATE_SEND_MESSAGE', )

    profile = models.ForeignKey('users.Profile', related_name='coin_histories', on_delete=models.CASCADE, null=True, blank=True)

    rest_coin = models.PositiveSmallIntegerField()
    reason = models.CharField(max_length=50, choices=CHANGE_REASON)
    message = models.CharField(max_length=200)
