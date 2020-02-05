from django.db import models

from common.models import BaseModel


# Create your models here.
class CoinHistory(BaseModel):
    CHANGE_REASON = (
        ('Signup', 'SignUp'),
        ('Consume', 'Consume'),
        ('Refund', 'Refund'),
    )
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    rest_coin = models.IntegerField()
    reason = models.CharField(max_length=50, choices=CHANGE_REASON)
