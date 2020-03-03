from django.db import transaction
from django_rest_framework_mango.mixins import PermissionMixin, SerializerMixin
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from profiles.serializers import CreateProfileSerializer
from self_date.serializer import CreateSignupCoinHistorySerializer
from users.models import User
from users.permissions import IsSameUserWithRequestUser
from users.serializers import UserSerializer, TokenSerializer, UserCheckUnivSerializer
from common.constants import SIGNUP_COIN
from self_date.models import CoinHistory


class UserViewSet(
    PermissionMixin, SerializerMixin,
    UpdateModelMixin, DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = User.objects.all()
    permission_classes = (IsSameUserWithRequestUser,)
    permission_by_actions = {
        'tokens': (AllowAny,),
        'create': (AllowAny,),
        'confirm_user': (AllowAny,),
    }
    serializer_class_by_actions = {
        'tokens': TokenSerializer,
        'create': UserSerializer,
        'update': UserSerializer,
        'partial_update': UserSerializer,
        'check_email': UserCheckUnivSerializer,
    }

    @action(detail=False, methods=['post'])
    def tokens(self, request, *args, **kwargs):
        token_obtain_pair_serializer = TokenObtainPairSerializer(data=request.data)

        token_obtain_pair_serializer.is_valid(raise_exception=True)
        token_with_profile = {
            **token_obtain_pair_serializer.validated_data,
            'profile': User.objects.get(email=request.data['email']).profile
        }

        serializer = self.get_serializer(token_with_profile)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        user_serializer = self.get_serializer(data=request.data)
        user_serializer.is_valid(raise_exception=True)
        created_user = user_serializer.save()
        created_user.set_user_code()
        created_user.save()

        profile_data = {
            'user': created_user.id,
            **request.data,
        }

        profile_serializer = CreateProfileSerializer(data=profile_data)
        profile_serializer.is_valid(raise_exception=True)
        profile_serializer.save()

        coin_history_data = {
            'user': created_user.id,
            'rest_coin': SIGNUP_COIN,
            'reason': CoinHistory.CHANGE_REASON.SIGNUP,
        }

        coin_history_serializer = CreateSignupCoinHistorySerializer(data=coin_history_data)
        coin_history_serializer.is_valid(raise_exception=True)
        coin_history_serializer.save()

        return Response(user_serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['patch'], url_path='check-univ')
    def check_email(self, request, *arg, **kwargs):
        user = self.get_object()
        update_response = self.partial_update(request, *arg, **kwargs)
        # Todo(10000001a): 성공과 실패를 분기하면 더 좋을 것 같다.
        user.send_email()

        return update_response

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        user.deactivate()

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['post'], url_path='confirm-user')
    def confirm_user(self, request, *arg, **kwargs):
        user_code = request.data['user_code']
        try:
            user = self.get_queryset().get(user_code=user_code)
            user.confirm_student()

            return Response(user_code, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(user_code, status=status.HTTP_400_BAD_REQUEST)
