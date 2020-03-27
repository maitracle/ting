from django.db import models

from common.models import BaseModel
from common.models import BaseModel
from users.models import User


class Like(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    liked_user = models.ForeignKey(User, related_name='liked_user', on_delete=models.CASCADE)



