from django_rest_framework_mango.mixins import PermissionMixin, SerializerMixin
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin, CreateModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from coins.models import CoinHistory
from common.permissions import IsOwnerUserOrReadonly
from users.models import User, Profile
from users.permissions import IsSameUserWithRequestUser
from users.serializers.profiles import ProfileSerializer
from users.serializers.users import UserSerializer, TokenSerializer, UserCheckUnivSerializer, MySerializer


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
        'my': MySerializer,
    }

    @action(detail=False, methods=['post'])
    def tokens(self, request, *args, **kwargs):
        token_obtain_pair_serializer = TokenObtainPairSerializer(data=request.data)

        token_obtain_pair_serializer.is_valid(raise_exception=True)
        user = User.objects.get(email=request.data['email'])
        coin_history_list = CoinHistory.objects.filter(user=user).order_by('-id')
        response_data = {
            **token_obtain_pair_serializer.validated_data,
            'user': user,
            'profile': getattr(user, 'profile', None),
            'coin_history': coin_history_list,
        }

        serializer = self.get_serializer(response_data)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        user_serializer = self.get_serializer(data=request.data)
        user_serializer.is_valid(raise_exception=True)
        created_user = user_serializer.save()

        created_user.set_user_code()
        created_user.set_password(request.data['password'])
        created_user.save()

        refresh = RefreshToken.for_user(created_user)

        response_data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': user_serializer.data,
        }

        return Response(response_data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        user.deactivate()

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['patch'], url_path='check-univ')
    def check_email(self, request, *arg, **kwargs):
        update_response = self.partial_update(request, *arg, **kwargs)
        user = self.get_object()
        # Todo(10000001a): 성공과 실패를 분기하면 더 좋을 것 같다.
        user.send_email()

        return update_response

    @action(detail=False, methods=['post'], url_path='confirm-user')
    def confirm_user(self, request, *arg, **kwargs):
        user_code = request.data['user_code']
        try:
            user = self.get_queryset().get(user_code=user_code)
            user.confirm_student()

            return Response(user_code, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(user_code, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def my(self, request, *args, **kwargs):
        data = {
            'user': request.user,
            'profile': getattr(request.user, 'profile', None),
            'coin_history': CoinHistory.objects.filter(user=request.user).order_by('-id'),

        }
        serializer = self.get_serializer(data)
        return Response(serializer.data)


class ProfileViewSet(
    CreateModelMixin, UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Profile.objects.all()
    permission_classes = (IsOwnerUserOrReadonly,)
    serializer_class = ProfileSerializer
