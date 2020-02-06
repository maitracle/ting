from django.db import models
from model_utils import Choices

from common.models import BaseModel
from common.models import BaseModel
from users.models import User


class Like(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    liked_user = models.ForeignKey(User, related_name='liked_user', on_delete=models.CASCADE)


class CoinHistory(BaseModel):
    CHANGE_REASON = Choices('SIGNUP', 'CONSUME', 'REFUND', )

    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    rest_coin = models.IntegerField()
    reason = models.CharField(max_length=50, choices=CHANGE_REASON)
