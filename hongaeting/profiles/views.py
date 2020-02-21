from django_filters.rest_framework import DjangoFilterBackend
from django_rest_framework_mango.mixins import QuerysetMixin, SerializerMixin
from rest_framework import viewsets
from rest_framework.mixins import ListModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticated

from profiles.models import Profile
from profiles.serializers import ListProfileSerializer, UpdateProfileSerializer, CreateProfileSerializer


class ProfileViewSet(
    QuerysetMixin, SerializerMixin,
    UpdateModelMixin, ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Profile.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateProfileSerializer
    serializer_class_by_actions = {
        'list': ListProfileSerializer,
        'update': UpdateProfileSerializer,
    }
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('gender', 'user__university',)

    def list_queryset(self, queryset):
        return queryset.filter(is_active=True)
