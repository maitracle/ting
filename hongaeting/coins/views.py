from django.shortcuts import render
from django_rest_framework_mango.mixins import QuerysetMixin
from rest_framework import viewsets, filters
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticated

from coins.models import CoinHistory
from coins.serializers import ListCoinHistorySerializer


class CoinHistoryViewSet(
    QuerysetMixin,
    ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = CoinHistory.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ListCoinHistorySerializer
    filter_backends = [filters.OrderingFilter]
    ordering = ['-id', ]

    def filtered_queryset_by_user(self, queryset):
        return queryset.filter(user=self.request.user)

    def list_queryset(self, queryset):
        return self.filtered_queryset_by_user(queryset)