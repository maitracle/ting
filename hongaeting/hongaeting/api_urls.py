from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenRefreshView

from profiles.views import SelfDateProfileViewSet
from self_date.views import CoinHistoryViewSet, LikeViewSet
from users.views import UserViewSet

router = SimpleRouter()
router.register('users', UserViewSet)
router.register('coin-histories', CoinHistoryViewSet)
router.register('likes', LikeViewSet)
router.register('self-dates', SelfDateProfileViewSet)

urlpatterns = [
    path('users/tokens/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns += router.urls
