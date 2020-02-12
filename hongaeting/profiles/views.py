from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from django_rest_framework_mango.mixins import QuerysetMixin
from rest_framework import viewsets
from rest_framework.mixins import CreateModelMixin, ListModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticated

from profiles.models import QuestionList, QuestionItem, Profile
from profiles.serializer import ProfileSerializer


class QuestionListViewSet(
    CreateModelMixin, ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = QuestionList.objects.all()

    def filtered_queryset_by_name(self, queryset):
        return queryset.filter(user=self.request.name)

    def list_queryset(self, queryset):
        return self.filtered_queryset_by_name(queryset)


class QuestionItemViewSet(
    CreateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = QuestionItem.objects.all()


class ProfileViewSet(
    QuerysetMixin,
    CreateModelMixin, UpdateModelMixin, ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Profile.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer
    filter_backends = (DjangoFilterBackend, )
    filterset_fields = ('gender', 'user__university', )

    def list_queryset(self, queryset):
        return queryset.filter(is_active=True)