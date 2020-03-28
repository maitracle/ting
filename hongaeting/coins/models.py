from django.db import models
from model_utils import Choices

from common.models import BaseModel


class CoinHistory(BaseModel):
    CHANGE_REASON = Choices('SIGNUP', 'VIEW_PROFILE', 'SEND_MESSAGE', )

    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    rest_coin = models.PositiveSmallIntegerField()
    reason = models.CharField(max_length=50, choices=CHANGE_REASON)
    profile = models.ForeignKey('self_date.SelfDateProfile', on_delete=models.DO_NOTHING, null=True, blank=True)
