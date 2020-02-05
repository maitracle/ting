from django_rest_framework_mango.mixins import QuerysetMixin
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.response import Response

from self_date.models import CoinHistory
from self_date.serializer import CreateCoinHistorySerializer


class CoinHistoryViewSet(
    CreateModelMixin, ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = CoinHistory.objects.all()
    serializer_class = CreateCoinHistorySerializer

    @action(detail=False, methods=['get'], url_path='users/(?P<user_id>\d+)/coin-histoires')
    def get_coin_history_list_by_user(self, request, user_id, *args, **kwargs):
        coin_history_queryset = self.get_queryset()
        coin_history_filtered_queryset = coin_history_queryset.filter(user_id=user_id)
        coin_history_serializer = self.get_serializer(data=coin_history_filtered_queryset)

        if coin_history_serializer.is_valid():
            coin_history_list = coin_history_serializer.validated_data
            return Response(status=status.HTTP_200_OK, data={
                'coin_history_list': coin_history_list
            })

        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
