from django_rest_framework_mango.mixins import PermissionMixin
from rest_framework import viewsets, status
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, DestroyModelMixin, RetrieveModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from users.models import User
from users.serializers import CreateUserSerializer


class UserViewSet(
    PermissionMixin,
    CreateModelMixin, UpdateModelMixin, RetrieveModelMixin, DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = (AllowAny, )
    permission_by_actions = {
        'create': (AllowAny, ),
        'destroy': (AllowAny, ),
    }

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.deactivate()

        return Response(status=status.HTTP_204_NO_CONTENT)
