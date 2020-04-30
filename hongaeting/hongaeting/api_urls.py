from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenRefreshView
from coins.views import CoinHistoryViewSet
from self_date.views import SelfDateLikeViewSet, SelfDateProfileViewSet
from users.views import UserViewSet, ProfileViewSet

router = SimpleRouter()
router.register('users', UserViewSet)
router.register('profiles', ProfileViewSet)
router.register('coin-histories', CoinHistoryViewSet)
router.register('self-date-likes', SelfDateLikeViewSet)
router.register('self-date-profiles', SelfDateProfileViewSet)

urlpatterns = [
    path('users/tokens/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns += router.urls
