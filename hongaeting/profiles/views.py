from django.shortcuts import render
from rest_framework.mixins import CreateModelMixin

from profiles.models import QuestionList


class QuestionListViewset(
  CreateModelMixin
):
    queryset = QuestionList.objects.all()
