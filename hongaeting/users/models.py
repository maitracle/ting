import datetime
import os

from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models, transaction
from django.template.loader import render_to_string
from django.utils.crypto import get_random_string
from model_utils import Choices

from common.constants import UNIVERSITY_CHOICES, REWORD_COUNT, COIN_CHANGE_REASON
from common.models import BaseModel
from common.utils import Email


def student_id_card_image_path(instance, original_filename):
    path = f'id_cards/{instance.get_full_name()}/image{os.path.splitext(original_filename)[1]}'
    return path


class NullableEmailField(models.EmailField):
    description = "EmailField that stores NULL but returns ''"

    def to_python(self, value):
        if isinstance(value, models.EmailField):
            return value
        return value or ''

    def get_prep_value(self, value):
        return value or None


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

    university_email = NullableEmailField(max_length=100, null=True, blank=True, unique=True,
                                          help_text='학교 인증을 위한 메일')
    student_id_card_image = models.ImageField(upload_to=student_id_card_image_path, blank=True, null=True,
                                              max_length=1000, verbose_name='학생증 사진')
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

    @transaction.atomic()
    def confirm_student(self):
        self.is_confirmed_student = True

        profile = getattr(self, 'profile', None)

        if profile:
            profile.change_coin_count(self.profile.get_rest_coin() + REWORD_COUNT['CONFIRM_USER'],
                                      COIN_CHANGE_REASON.CONFIRM_USER,
                                      '학생 인증으로 인한 coin 지급')

        self.save()

    def send_email(self):
        # Todo(10000001a): Email template 다시 작업해야함
        html_content = render_to_string('mail_template.html',
                                        {'user_code': self.user_code,
                                         'front_address':
                                             f'{settings.FRONT_END_URL}{settings.FRONT_END_MAIL_CHECK_PAGE}'})
        Email.send_email(f'{self.university_email}님 학생 인증을 완료해주세요.', html_content, self.university_email)

    def set_user_code(self):
        user_code = get_random_string(length=8)
        same_user_code_queryset = User.objects.filter(user_code=user_code)
        if not same_user_code_queryset.exists():
            self.user_code = user_code
        else:
            self.set_user_code()


def max_value_current_year(value):
    return MaxValueValidator(datetime.date.today().year)(value)


class Profile(BaseModel):
    GENDER_CHOICES = Choices('MALE', 'FEMALE')
    SCHOLARLY_STATUS_CHOICES = Choices('ATTENDING', 'TAKING_OFF')
    CAMPUS_LOCATION_CHOICES = Choices('SEOUL', 'INTERNATIONAL', 'SINCHON')

    user = models.OneToOneField('users.User', on_delete=models.CASCADE, verbose_name='사용자')

    nickname = models.CharField(max_length=8, unique=True, verbose_name='공통닉네임')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, verbose_name='성별')
    born_year = models.SmallIntegerField(validators=[MinValueValidator(1980), max_value_current_year],
                                         verbose_name='태어난 년도')

    university = models.CharField(max_length=10, blank=True, null=True, choices=UNIVERSITY_CHOICES, verbose_name='학교')
    campus_location = models.CharField(max_length=20, choices=CAMPUS_LOCATION_CHOICES, verbose_name='캠퍼스')
    scholarly_status = models.CharField(max_length=10, choices=SCHOLARLY_STATUS_CHOICES, verbose_name='재학여부')

    def __str__(self):
        return self.nickname

    @property
    def age(self):
        korean_age_correction = 1
        return datetime.datetime.now().year - self.born_year + korean_age_correction

    def change_coin_count(self, change_amount, reason, message=''):
        from coins.models import CoinHistory

        return CoinHistory.objects.create(profile=self, rest_coin=self.get_rest_coin() + change_amount, reason=reason,
                                          message=message)

    def get_rest_coin(self):
        """이 프로필이 가지고있는 coin 개수를 반환한다."""
        from coins.models import CoinHistory

        last_coin_history = CoinHistory.objects.filter(profile=self).last()

        return last_coin_history.rest_coin if last_coin_history else 0
