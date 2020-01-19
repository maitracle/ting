from django.conf import settings
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView


class HealthView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        data = {
            'Profile': settings.PROFILE,
        }

        return Response(data, status=status.HTTP_200_OK)
