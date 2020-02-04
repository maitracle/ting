from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, ListModelMixin

from self_date.models import CoinHistory
from self_date.serializer import CreateCoinHistorySerializer


class CoinHistoryViewSet(
    viewsets.GenericViewSet, CreateModelMixin, ListModelMixin
):
    queryset = CoinHistory.objects.all()
    serializer_class = CreateCoinHistorySerializer