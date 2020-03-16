from django_rest_framework_mango.mixins import QuerysetMixin
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from common.permissions import IsOwnerUserOrReadonly
from self_date.models import CoinHistory, Like
from self_date.serializer import ListCoinHistorySerializer, LikeSerializer


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


class LikeViewSet(
    QuerysetMixin,
    ListModelMixin, DestroyModelMixin,
    viewsets.GenericViewSet
):
    queryset = Like.objects.all()
    permission_classes = (IsOwnerUserOrReadonly,)
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
