from rest_framework import generics, permissions

from apps.accounts.models import User

from .serializers import RegisterAccountSerializer


class RegisterAccountAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterAccountSerializer
    permission_classes = (permissions.AllowAny,)
