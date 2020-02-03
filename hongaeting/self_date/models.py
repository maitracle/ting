from django.db import models

from users.models import User
from common.models import BaseModel

class Like(BaseModel):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    liked_user = models.ForeignKey(User, related_name='liked_user', on_delete=models.DO_NOTHING)

# Create your models here.
