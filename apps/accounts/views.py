from rest_framework import generics, mixins, permissions, viewsets

from .models import User
from .serializers import AccountSerializer


class AccountViewSet(
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = User.objects.all()
    serializer_class = AccountSerializer
    permission_classes = []

    def get_queryset(self):
        return super().get_queryset().filter(pk=self.request.user.pk)
