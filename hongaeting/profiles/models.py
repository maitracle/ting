from django.db import models

from common.constants import UNIVERSITY_CHOICE, GENDER_CHOICE
from common.models import BaseModel


class QuestionList(BaseModel):
    name = models.CharField(max_length=30)
    university = models.CharField(max_length=30, choices=UNIVERSITY_CHOICE)
    season = models.IntegerField()
    version = models.IntegerField()

    def __str__(self):
        return self.name


class QuestionItem(BaseModel):
    name = models.CharField(max_length=100)
    question_list = models.ForeignKey('profiles.QuestionList', on_delete=models.CASCADE)
    question_number = models.PositiveSmallIntegerField()


class Profile(BaseModel):
    user = models.OneToOneField('users.User', on_delete=models.CASCADE)
    nickname = models.CharField()
    gender = models.CharField(choices=GENDER_CHOICE)
    age = models.PositiveSmallIntegerField()
    height = models.PositiveSmallIntegerField()
    body_shape = models.CharField()
    tag = models.CharField()
    image = models.CharField()
