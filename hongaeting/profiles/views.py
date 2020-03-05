from django.db.models import Count, Case, When, Value, BooleanField, Subquery, OuterRef
from django_filters.rest_framework import DjangoFilterBackend
from django_rest_framework_mango.mixins import QuerysetMixin, SerializerMixin
from rest_framework import viewsets
from rest_framework.mixins import ListModelMixin, UpdateModelMixin, RetrieveModelMixin

from common.permissions import IsOwnerUserOrReadonly
from profiles.models import Profile
from profiles.serializers import ListProfileSerializer, UpdateProfileSerializer, RetrieveProfileSerializer
from self_date.models import CoinHistory


class ProfileViewSet(
    QuerysetMixin, SerializerMixin,
    UpdateModelMixin, ListModelMixin, RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Profile.objects.all()
    permission_classes = (IsOwnerUserOrReadonly,)
    serializer_class_by_actions = {
        'list': ListProfileSerializer,
        'update': UpdateProfileSerializer,
        'partial_update': UpdateProfileSerializer,
        'retrieve': RetrieveProfileSerializer,
    }
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('gender', 'user__university',)

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
