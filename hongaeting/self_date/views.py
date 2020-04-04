from django.db.models import Count, Case, When, Value, BooleanField, Subquery, OuterRef
from django_filters.rest_framework import DjangoFilterBackend
from django_rest_framework_mango.mixins import QuerysetMixin, SerializerMixin
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.mixins import DestroyModelMixin, CreateModelMixin, ListModelMixin, UpdateModelMixin, \
    RetrieveModelMixin
from rest_framework.response import Response

from coins.models import CoinHistory
from coins.serializers import CreateCoinHistorySerializer
from common.constants import COIN_CHANGE_REASON
from common.permissions import IsOwnerProfileOrReadonly
from common.permissions import IsOwnerUserOrReadonly
from self_date.serializers import ListSelfDateProfileSerializer, UpdateSelfDateProfileSerializer, \
    RetrieveSelfDateProfileSerializer, LikeSerializer, CreateSelfDateProfileSerializer
from .models import SelfDateProfile, Like, SelfDateProfileRight


class SelfDateProfileViewSet(
    QuerysetMixin, SerializerMixin,
    CreateModelMixin, UpdateModelMixin, ListModelMixin, RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = SelfDateProfile.objects.all()
    permission_classes = (IsOwnerProfileOrReadonly,)
    serializer_class_by_actions = {
        'create': CreateSelfDateProfileSerializer,
        'list': ListSelfDateProfileSerializer,
        'update': UpdateSelfDateProfileSerializer,
        'partial_update': UpdateSelfDateProfileSerializer,
        'retrieve': RetrieveSelfDateProfileSerializer,
    }
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('profile__gender', 'profile__university',)

    def list_queryset(self, queryset):
        self_date_profile_right_queryset = SelfDateProfileRight.objects.filter(
            buying_self_date_profile=self.request.user.profile.selfdateprofile
        ).filter(
            right_type=COIN_CHANGE_REASON.SELF_DATE_PROFILE_VIEW
        ).filter(
            target_self_date_profile_id=OuterRef('id')
        )

        return queryset.filter(
            is_active=True
        ).annotate(
            view_count=Count(Subquery(self_date_profile_right_queryset.values('id')))
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
        request_self_date_profile = request.user.profile.selfdateprofile
        target_self_date_profile = self.get_object()

        response_self_date_profile = request_self_date_profile.get_target_self_date_profile_to_retrieve(target_self_date_profile)

        self_date_profile_serializer = self.get_serializer(response_self_date_profile)

        return Response(self_date_profile_serializer.data)

    @action(detail=True, methods=['get'], url_path='chat-link')
    def get_chat_link(self, request, *arg, **kwargs):
        profile = self.get_object()

        if not profile.is_valid_chat_link:
            return Response(status=status.HTTP_404_NOT_FOUND)

        is_sent = SelfDateProfileRight.objects.filter(
            buying_self_date_profile=self.request.user.profile.selfdateprofile,
            target_self_date_profile=profile,
            right_type=COIN_CHANGE_REASON.SELF_DATE_SEND_MESSAGE
        )

        if not is_sent:
            try:
                rest_coin = CoinHistory.objects.filter(user=request.user).last().rest_coin
                coin_history_data = {
                    'user': request.user.id,
                    'rest_coin': rest_coin - SEND_MESSAGE_COST,
                    'reason': CoinHistory.CHANGE_REASON.SEND_MESSAGE,
                    'profile': profile.id
                }

                coin_history_instance = CreateCoinHistorySerializer(data=coin_history_data)
                coin_history_instance.is_valid(raise_exception=True)
                coin_history_instance.save()
            except ValidationError:
                return Response(status=status.HTTP_403_FORBIDDEN)

        chat_link = {
            'chat_link': profile.chat_link,
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
