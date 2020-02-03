from django.db import models

from common.models import BaseModel


# Create your models here.
class CoinHistory(BaseModel):
    CHANGE_REASON = (
        ('Signup'),
        ('Consume'),
        ('Refund'),
    )
    user = models.ForeignKey('User', on_delete=models.DO_NOTHING)
    rest_coin = models.IntegerField()
    reason = models.CharField(max_length=50, choices=CHANGE_REASON)
