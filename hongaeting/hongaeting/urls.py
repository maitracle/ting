from django.contrib import admin
from django.urls import include
from django.urls import path

from common.views import HealthView

urlpatterns = [
    path('api/', include('hongaeting.api_urls')),
    path('admin/', admin.site.urls),
    path('health/', HealthView.as_view()),
]
