from django.core.validators import MinValueValidator, MinLengthValidator
from django.db import models
from model_utils import Choices

from common.constants import UNIVERSITY_LIST
from common.models import BaseModel


class QuestionList(BaseModel):
    name = models.CharField(max_length=30)
    university = models.CharField(max_length=30, choices=UNIVERSITY_LIST)
    season = models.IntegerField()
    version = models.IntegerField()

    def __str__(self):
        return self.name


class QuestionItem(BaseModel):
    name = models.CharField(max_length=100)
    question_list = models.ForeignKey('profiles.QuestionList', on_delete=models.CASCADE)
    question_number = models.PositiveSmallIntegerField()


class Profile(BaseModel):
    MAX_CHARFIELD_LENGTH = 300
    BODY_TYPE = Choices('SKINNY', 'SLIM', 'NORMAL', 'CHUBBY', 'FAT')
    GENDER_CHOICE = Choices('MALE', 'FEMALE')

    user = models.OneToOneField('users.User', on_delete=models.CASCADE)
    nickname = models.CharField(max_length=8, unique=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICE)
    age = models.PositiveSmallIntegerField(validators=[MinValueValidator(19)])
    height = models.PositiveSmallIntegerField()
    body_type = models.CharField(max_length=10, choices=BODY_TYPE)

    tag = models.CharField(max_length=100)
    image = models.CharField(max_length=100)

    appearance = models.CharField(max_length=MAX_CHARFIELD_LENGTH, validators=[MinLengthValidator(120)])
    personality = models.CharField(max_length=MAX_CHARFIELD_LENGTH, validators=[MinLengthValidator(120)])
    hobby = models.CharField(max_length=MAX_CHARFIELD_LENGTH, validators=[MinLengthValidator(120)])
    ideal_type = models.CharField(max_length=MAX_CHARFIELD_LENGTH, validators=[MinLengthValidator(120)])
    last_tempting_word = models.CharField(max_length=MAX_CHARFIELD_LENGTH, validators=[MinLengthValidator(120)])

    is_active = models.BooleanField(default=True)
