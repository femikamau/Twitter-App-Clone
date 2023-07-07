from rest_framework import mixins, viewsets

from apps.utils.viewsets import CreateListRetrieveDestroyViewSet

from .models import Friend
from .serializers import FriendSerializer


class FollowingViewSet(CreateListRetrieveDestroyViewSet):
    serializer_class = FriendSerializer

    def get_queryset(self):
        return Friend.objects.filter(from_user=self.request.user)


class FollowerViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = FriendSerializer

    def get_queryset(self):
        return Friend.objects.filter(to_user=self.request.user)
