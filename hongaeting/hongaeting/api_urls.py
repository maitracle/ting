from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.views import UserViewSet


router = SimpleRouter()
router.register('users', UserViewSet)


urlpatterns = [
    path('users/', include('users.urls')),
    path()
]
