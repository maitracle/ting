from django.db import models
from model_utils import Choices

from common.models import BaseModel


from users.models import User
from common.models import BaseModel

class Like(BaseModel):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    liked_user = models.ForeignKey(User, related_name='liked_user', on_delete=models.DO_NOTHING)

# Create your models here.
class CoinHistory(BaseModel):
    CHANGE_REASON = Choices('SIGNUP', 'CONSUME', 'REFUND', )

    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    rest_coin = models.IntegerField()
    reason = models.CharField(max_length=50, choices=CHANGE_REASON)
