from django_rest_framework_mango.mixins import QuerysetMixin
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.mixins import ListModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from common.constants import SEND_MESSAGE_COST
from common.permissions import IsOwnerUserOrReadonly
from self_date.models import CoinHistory, Like
from self_date.serializer import ListCoinHistorySerializer, LikeSerializer, CreateCoinHistorySerializer
from profiles.models import Kakao, Profile


class CoinHistoryViewSet(
    QuerysetMixin,
    ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = CoinHistory.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ListCoinHistorySerializer

    def filtered_queryset_by_user(self, queryset):
        return queryset.filter(user=self.request.user)

    def list_queryset(self, queryset):
        return self.filtered_queryset_by_user(queryset)

    @action(detail=True, methods=['post'], url_path='send-message')
    def send_message(self, request, *arg, **kwargs):
        profile = Profile.objects.get(id=int(kwargs['pk']))
        if not Kakao.is_valid_kakao_link(profile.chat_link):
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            isSent = CoinHistory.objects.filter(
                user=request.user,
                reason=CoinHistory.CHANGE_REASON.SEND_MESSAGE,
                profile=kwargs['pk']
            )
            rest_coin = CoinHistory.objects.filter(user=request.user).last().rest_coin
            if not isSent:
                try:
                    coin_history_data = {
                        "user": request.user.id,
                        "rest_coin": rest_coin - SEND_MESSAGE_COST,
                        "reason": CoinHistory.CHANGE_REASON.SEND_MESSAGE,
                        "profile": int(kwargs['pk'])
                    }

                    coin_history_instance = CreateCoinHistorySerializer(data=coin_history_data)
                    coin_history_instance.is_valid(raise_exception=True)
                    coin_history_instance.save()
                except ValidationError:
                    return Response(status=status.HTTP_403_FORBIDDEN)
            chat_link = {
                "chat_link": profile.chat_link,
            }
            return Response(chat_link)


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
