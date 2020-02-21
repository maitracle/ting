from django.db import transaction
from django_rest_framework_mango.mixins import PermissionMixin
from rest_framework import viewsets, status
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from profiles.serializers import CreateProfileSerializer
from users.models import User
from users.serializers import CreateUserSerializer


class UserViewSet(
    PermissionMixin,
    CreateModelMixin, UpdateModelMixin, DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = (AllowAny,)
    permission_by_actions = {
        'create': (AllowAny,),
        'destroy': (AllowAny,),
    }

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        user_data = {
            'email': request.data['email'],
            'password': request.data['password'],
            'university': request.data['university'],
            'university_email': request.data['university_email'],
        }

        sign_up_to_user_serializer = self.get_serializer(data=user_data)
        sign_up_to_user_serializer.is_valid(raise_exception=True)
        sign_up_to_user_serializer.save()

        created_user = User.objects.get(email=user_data['email']).id
        profile_data = {
            'user': created_user,
            'nickname': request.data['nickname'],
            'gender': request.data['gender'],
            'campus_location': request.data['campus_location'],
        }

        self.serializer_class = CreateProfileSerializer
        sign_up_to_profile_serializer = self.get_serializer(data=profile_data)
        sign_up_to_profile_serializer.is_valid(raise_exception=True)
        sign_up_to_profile_serializer.save()

        self.serializer_class = CreateUserSerializer
        return Response(request.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        user.deactivate()

        return Response(status=status.HTTP_204_NO_CONTENT)
