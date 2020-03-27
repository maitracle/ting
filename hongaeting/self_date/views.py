from django.db.models import Count, Case, When, Value, BooleanField, Subquery, OuterRef
from django_filters.rest_framework import DjangoFilterBackend
from django_rest_framework_mango.mixins import QuerysetMixin, SerializerMixin
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.mixins import DestroyModelMixin
from rest_framework.mixins import ListModelMixin, UpdateModelMixin, RetrieveModelMixin
from rest_framework.response import Response

from coins.models import CoinHistory
from coins.serializers import CreateCoinHistorySerializer
from common.constants import VIEW_PROFILE_COST, SEND_MESSAGE_COST
from common.permissions import IsOwnerProfileOrReadonly
from common.permissions import IsOwnerUserOrReadonly
from self_date.serializers import ListSelfDateProfileSerializer, UpdateSelfDateProfileSerializer, \
    RetrieveSelfDateProfileSerializer
from self_date.serializers import LikeSerializer
from .models import SelfDateProfile, Like


class SelfDateProfileViewSet(
    QuerysetMixin, SerializerMixin,
    UpdateModelMixin, ListModelMixin, RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = SelfDateProfile.objects.all()
    permission_classes = (IsOwnerProfileOrReadonly,)
    serializer_class_by_actions = {
        'list': ListSelfDateProfileSerializer,
        'update': UpdateSelfDateProfileSerializer,
        'partial_update': UpdateSelfDateProfileSerializer,
        'retrieve': RetrieveSelfDateProfileSerializer,
    }
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('profile__gender', 'profile__university',)

    def list_queryset(self, queryset):
        coin_history_queryset = CoinHistory.objects.filter(user=self.request.user).filter(
            reason=CoinHistory.CHANGE_REASON.VIEW_PROFILE) \
            .filter(profile_id=OuterRef('id'))

        return queryset.filter(
            is_active=True
        ).annotate(
            view_count=Count(Subquery(coin_history_queryset.values('id')))
        ).annotate(
            is_viewed=Case(
                When(view_count__gt=0,
                     then=Value(True)
                     ),
                default=Value(False),
                output_field=BooleanField()
            )
        )

    def retrieve(self, request, *args, **kwargs):
        isViewed = CoinHistory.objects.filter(
            user=request.user,
            reason=CoinHistory.CHANGE_REASON.VIEW_PROFILE,
            profile=kwargs['pk']
        ).exists()

        if not isViewed:
            try:
                rest_coin = CoinHistory.objects.filter(user=request.user).last().rest_coin
                coin_history_data = {
                    "user": request.user.id,
                    "rest_coin": rest_coin - VIEW_PROFILE_COST,
                    "reason": CoinHistory.CHANGE_REASON.VIEW_PROFILE,
                    "profile": int(kwargs['pk'])
                }

                coin_history_instance = CreateCoinHistorySerializer(data=coin_history_data)
                coin_history_instance.is_valid(raise_exception=True)
                coin_history_instance.save()

            except ValidationError:
                return Response(status=status.HTTP_403_FORBIDDEN)

        profile = self.get_object()
        profile_serializer = self.get_serializer(profile)

        return Response(profile_serializer.data)

    @action(detail=True, methods=['get'], url_path='chat-link')
    def get_chat_link(self, request, *arg, **kwargs):
        profile = self.get_object()
        if not profile.is_valid_chat_link:
            return Response(status=status.HTTP_404_NOT_FOUND)
        isSent = CoinHistory.objects.filter(
            user=request.user,
            reason=CoinHistory.CHANGE_REASON.SEND_MESSAGE,
            profile=profile.id
        )
        if not isSent:
            try:
                rest_coin = CoinHistory.objects.filter(user=request.user).last().rest_coin
                coin_history_data = {
                    "user": request.user.id,
                    "rest_coin": rest_coin - SEND_MESSAGE_COST,
                    "reason": CoinHistory.CHANGE_REASON.SEND_MESSAGE,
                    "profile": profile.id
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
