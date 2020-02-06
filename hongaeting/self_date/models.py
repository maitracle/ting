from django.db import models
from model_utils import Choices

from common.models import BaseModel


# Create your models here.
class CoinHistory(BaseModel):
    CHANGE_REASON = Choices('SIGNUP', 'CONSUME', 'REFUND', )

    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    rest_coin = models.IntegerField()
    reason = models.CharField(max_length=50, choices=CHANGE_REASON)
