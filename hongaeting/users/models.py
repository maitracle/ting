from django.contrib.auth.models import AbstractUser
from django.db import models

from common.models import BaseModel


class User(BaseModel, AbstractUser):
    confirmed_email = models.BooleanField(default=False)
    user_code = models.CharField(max_length=10, blank=True)

    def deactivate(self):
        self.is_active = False
