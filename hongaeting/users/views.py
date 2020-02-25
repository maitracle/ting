from django.db import transaction
from django_rest_framework_mango.mixins import PermissionMixin
from rest_framework import viewsets, status
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action

from profiles.serializers import CreateProfileSerializer
from users.models import User
from users.serializers import CreateUserSerializer


class UserViewSet(
    PermissionMixin,
    UpdateModelMixin, DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
    # serializer_class_by_actions = {
    #     'check_email':
    # }
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

        user_serializer = self.get_serializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user_instance = user_serializer.save()
        user_instance.set_user_code()
        user_instance.save()

        created_user = User.objects.get(email=user_data['email']).id
        profile_data = {
            'user': created_user,
            'nickname': request.data['nickname'],
            'gender': request.data['gender'],
            'campus_location': request.data['campus_location'],
        }

        profile_serializer = CreateProfileSerializer(data=profile_data)
        profile_serializer.is_valid(raise_exception=True)
        profile_serializer.save()

        return Response(user_serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['patch'], url_path='check-univ')
    def check_email(self, request, *arg, **kwargs):
        user = self.get_object()
        update_response = self.partial_update(request, *arg, **kwargs)
        user.send_email()

        return update_response

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        user.deactivate()

        return Response(status=status.HTTP_204_NO_CONTENT)
