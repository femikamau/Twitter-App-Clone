from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.friends.models import Friend
from apps.posts.models import Post
from apps.posts.serializers.posts import ReadPostSerializer, WritePostSerializer
from apps.utils.permissions import IsOwnerOrReadOnly

from .models import Profile
from .serializers import ListProfileSerializer, RetrieveProfileSerializer


class ProfileViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Profile.objects.all()
    serializer_class = ListProfileSerializer
    lookup_field = "user__username"
    permission_classes = (IsOwnerOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("$user__username",)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return RetrieveProfileSerializer

        if self.action == "posts":
            return WritePostSerializer

        return super().get_serializer_class()

    @action(methods=["GET", "POST"], detail=True)
    def posts(self, request, user__username):
        username = user__username

        if request.method == "GET":
            posts = Post.objects.filter(user__username=username)

            page = self.paginate_queryset(posts)

            if page is not None:
                serializer = ReadPostSerializer(
                    page,
                    many=True,
                    context={"request": request},
                )

                return self.get_paginated_response(serializer.data)

            serializer = ReadPostSerializer(
                posts,
                many=True,
                context={"request": request},
            )

            return Response(serializer.data, status=status.HTTP_200_OK)

        elif request.method == "POST":
            if request.user.username != username:
                return Response(
                    {"detail": "You do not have permission to perform this action"},
                    status=status.HTTP_403_FORBIDDEN,
                )

            serializer = WritePostSerializer(
                data=request.data,
                context={"request": request},
            )

            serializer.is_valid(raise_exception=True)

            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=["GET"], detail=True)
    def followers(self, request, user__username):
        username = user__username

        followers = Friend.objects.filter(to_user__username=username).values_list(
            "from_user", flat=True
        )

        profiles = Profile.objects.filter(user__in=followers)

        page = self.paginate_queryset(profiles)

        if page is not None:
            serializer = ListProfileSerializer(
                page,
                many=True,
                context={"request": request},
            )

            return self.get_paginated_response(serializer.data)

    @action(methods=["GET"], detail=True)
    def following(self, request, user__username):
        username = user__username

        following = Friend.objects.filter(from_user__username=username).values_list(
            "to_user", flat=True
        )

        profiles = Profile.objects.filter(user__in=following)

        page = self.paginate_queryset(profiles)

        if page is not None:
            serializer = ListProfileSerializer(
                page,
                many=True,
                context={"request": request},
            )

            return self.get_paginated_response(serializer.data)

    @action(detail=True)
    def follow(self, request, user__username):
        username = user__username

        if request.user.username == username:
            return Response(
                {"detail": "You can't follow yourself"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        profile = Profile.objects.get(user__username=username)

        friend, created = Friend.objects.get_or_create(
            from_user=request.user, to_user=profile.user
        )

        if created:
            return Response(
                {"detail": f"You are now following {profile.user.username}"},
                status=status.HTTP_200_OK,
            )

        return Response(
            {"detail": f"You are already following {profile.user.username}"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @action(detail=True)
    def unfollow(self, request, user__username):
        username = user__username

        if request.user.username == username:
            return Response(
                {"detail": "You can't unfollow yourself"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        profile = Profile.objects.get(user__username=username)

        friend = Friend.objects.filter(from_user=request.user, to_user=profile.user)

        if friend.exists():
            friend.delete()

            return Response(
                {"detail": f"You have unfollowed {profile.user.username}"},
                status=status.HTTP_200_OK,
            )

        return Response(
            {"detail": f"You are not following {profile.user.username}"},
            status=status.HTTP_400_BAD_REQUEST,
        )
