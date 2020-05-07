from django.db.models import Count, Case, When, Value, BooleanField, Subquery, OuterRef
from django_filters.rest_framework import DjangoFilterBackend
from django_rest_framework_mango.mixins import QuerysetMixin, SerializerMixin, PermissionMixin
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.mixins import DestroyModelMixin, CreateModelMixin, ListModelMixin, UpdateModelMixin, \
    RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from common.constants import COIN_CHANGE_REASON
from common.permissions import IsOwnerProfileOrReadonly, IsConfirmedUser
from self_date.serializers import ListSelfDateProfileSerializer, UpdateSelfDateProfileSerializer, \
    RetrieveSelfDateProfileSerializer, SelfDateLikeSerializer, CreateSelfDateProfileSerializer
from .models import SelfDateProfile, SelfDateProfileRight, SelfDateLike
from users.models import Profile


class IsHaveSelfDateProfileAndIsActive(permissions.BasePermission):
    message = 'Activated self date profile is needed'

    def has_permission(self, request, view):
        return hasattr(request.user.profile, 'self_date_profile') and request.user.profile.self_date_profile.is_active


class SelfDateProfileViewSet(
    QuerysetMixin, SerializerMixin, PermissionMixin,
    CreateModelMixin, UpdateModelMixin, ListModelMixin, RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = SelfDateProfile.objects.all()
    permission_classes = (IsOwnerProfileOrReadonly,)
    permission_by_actions = {
        'retrieve': (IsConfirmedUser, IsHaveSelfDateProfileAndIsActive,),
    }
    serializer_class_by_actions = {
        'create': CreateSelfDateProfileSerializer,
        'list': ListSelfDateProfileSerializer,
        'update': UpdateSelfDateProfileSerializer,
        'partial_update': UpdateSelfDateProfileSerializer,
        'retrieve': RetrieveSelfDateProfileSerializer,
        'my': RetrieveSelfDateProfileSerializer,
    }
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('profile__gender', 'profile__university',)

    def list_queryset(self, queryset):
        self_date_profile_right_queryset = SelfDateProfileRight.objects.filter(
            buying_self_date_profile=self.request.user.profile.self_date_profile
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
        request_self_date_profile = request.user.profile.self_date_profile
        target_self_date_profile = self.get_object()

        response_self_date_profile = request_self_date_profile.get_target_self_date_profile_to_retrieve(
            target_self_date_profile)

        self_date_profile_serializer = self.get_serializer(response_self_date_profile)

        return Response(self_date_profile_serializer.data)

    @action(detail=True, methods=['get'], url_path='chat-link')
    def get_chat_link(self, request, *arg, **kwargs):
        request_self_date_profile = request.user.profile.self_date_profile
        target_self_date_profile = self.get_object()

        response_target_chat_link = request_self_date_profile.get_target_chat_link(target_self_date_profile)
        chat_link = {
            'chat_link': response_target_chat_link,
        }

        return Response(chat_link)

    @action(detail=False, methods=['get'], url_path='my')
    def my(self, request, *arg, **kwargs):
        try:
            self_date_profile = getattr(request.user.profile, 'self_date_profile')
            my_self_date_profile_serializer = self.get_serializer(self_date_profile)
        except Profile.self_date_profile.RelatedObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(my_self_date_profile_serializer.data)


class SelfDateLikeViewSet(
    QuerysetMixin,
    ListModelMixin, DestroyModelMixin,
    viewsets.GenericViewSet
):
    queryset = SelfDateLike.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = SelfDateLikeSerializer

    def list_queryset(self, queryset):
        return queryset.filter(self_date_profile=self.request.user.profile.self_date_profile)

    def get_liked_queryset(self, queryset):
        return queryset.filter(liked_self_date_profile=self.request.user.profile.self_date_profile)

    @action(detail=False, methods=['get'], url_path='liked')
    def get_liked(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        data = {
            'self_date_profile': request.user.profile.self_date_profile.id,
            'liked_self_date_profile': request.data['liked_self_date_profile'],
        }
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
