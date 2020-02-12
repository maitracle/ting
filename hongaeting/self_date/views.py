from django_rest_framework_mango.mixins import QuerysetMixin, SerializerMixin
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, CreateModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from self_date.models import CoinHistory, Like
from self_date.serializer import CreateCoinHistorySerializer, ListCoinHistorySerializer, LikeSerializer


class CoinHistoryViewSet(
    QuerysetMixin, SerializerMixin,
    ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = CoinHistory.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ListCoinHistorySerializer
    serializer_class_by_actions = {
        'list': ListCoinHistorySerializer,
        'consume': CreateCoinHistorySerializer,
        'refund': CreateCoinHistorySerializer,
    }

    @action(detail=False, methods=['post'])
    def consume(self, request):
        last_coin_history = self.get_queryset().last()
        data = {
            "user": request.user.id,
            "rest_coin": last_coin_history.rest_coin - 1,
            "reason": CoinHistory.CHANGE_REASON.CONSUME,
        }

        return self._create_coin_history(data)

    @action(detail=False, methods=['post'])
    def refund(self, request):
        last_coin_history = self.get_queryset().last()
        data = {
            "user": request.user.id,
            "rest_coin": last_coin_history.rest_coin + 1,
            "reason": CoinHistory.CHANGE_REASON.REFUND,
        }

        return self._create_coin_history(data)

    def filtered_queryset_by_user(self, queryset):
        return queryset.filter(user=self.request.user)

    def list_queryset(self, queryset):
        return self.filtered_queryset_by_user(queryset)

    def consume_queryset(self, queryset):
        return self.filtered_queryset_by_user(queryset)

    def _create_coin_history(self, data):
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class LikeViewSet(
    QuerysetMixin,
    ListModelMixin, DestroyModelMixin,
    viewsets.GenericViewSet
):
    queryset = Like.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = LikeSerializer

    def list_queryset(self, queryset):
        return queryset.filter(user=self.request.user)

    def get_liked_queryset(self, queryset):
        return queryset.filter(liked_user=self.request.user)

    @action(detail=False, methods=['get'], url_path='liked')
    def get_liked(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        data = {
            'user': request.user.id,
            'liked_user': request.data['liked_user'],
        }
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
