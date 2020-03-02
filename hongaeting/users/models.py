from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from django.template.loader import render_to_string
from django.utils.crypto import get_random_string

from common.constants import UNIVERSITY_LIST
from common.models import BaseModel
from common.utils import Email


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

    def confirm_student(self):
        self.is_confirmed_student = True
        self.save()

    def send_email(self):
        # Todo(10000001a): Email template 다시 작업해야함
        html_content = render_to_string('mail_template.html', {'user_code': self.user_code})
        Email.send_email('title', html_content, [self.university_email])

    def set_user_code(self):
        user_code = get_random_string(length=8)
        same_user_code_queryset = User.objects.filter(user_code=user_code)
        if not same_user_code_queryset.exists():
            self.user_code = user_code
        else:
            self.set_user_code()
