from django_rest_framework_mango.mixins import PermissionMixin
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from users.models import User
from users.serializers import CreateUserSerializer


class UserViewSet(
    PermissionMixin,
    CreateModelMixin, UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = (IsAuthenticated, )
    permission_by_actions = {
        'create': (AllowAny, ),
    }

    @action()
    def deactivate(self, request, *args, **kwargs):
        instance = self.get_object()
        return Response(status=status.HTTP_204_NO_CONTENT)
        # is_active
