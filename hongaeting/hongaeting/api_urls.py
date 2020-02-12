from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from profiles.views import ProfileViewSet, QuestionListViewSet, QuestionItemViewSet
from self_date.views import CoinHistoryViewSet, LikeViewSet
from users.views import UserViewSet

router = SimpleRouter()
router.register('users', UserViewSet)
router.register('coin-histories', CoinHistoryViewSet)
router.register('likes', LikeViewSet)
router.register('profiles', ProfileViewSet)
router.register('question-lists', QuestionListViewSet)
router.register('question-items', QuestionItemViewSet)

urlpatterns = [
    path('tokens/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('tokens/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns += router.urls
