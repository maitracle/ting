from django.urls import path
from rest_framework.routers import SimpleRouter

from self_date.views import CoinHistoryViewSet

router = SimpleRouter()
router.register('', CoinHistoryViewSet)

urlpatterns = []
urlpatterns += router.urls
