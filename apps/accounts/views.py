from rest_framework import permissions, viewsets

from .models import User
from .serializers import AccountSerializer


class AccountViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = AccountSerializer
