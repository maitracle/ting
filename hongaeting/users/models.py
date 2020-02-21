from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models

from common.constants import UNIVERSITY_LIST
from common.models import BaseModel


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=UserManager.normalize_email(email),
        )

        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password):
        user = self.create_user(email=email,
                                password=password,
                                )
        user.is_staff = True
        user.is_superuser = True
        user.save()

        return user


class User(BaseModel, AbstractBaseUser):

    email = models.EmailField(max_length=100, unique=True)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    university = models.CharField(max_length=10, blank=True, null=True, choices=UNIVERSITY_LIST)
    university_email = models.EmailField(max_length=100, blank=True, help_text='학교 인증을 위한 메일')
    is_confirmed_student = models.BooleanField(default=False, help_text='학교 인증을 받았는지 여부')

    user_code = models.CharField(max_length=10, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def deactivate(self):
        self.is_active = False
        self.save()


