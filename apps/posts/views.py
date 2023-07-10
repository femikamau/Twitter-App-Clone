from django.db.models import Q
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.utils.permissions import IsOwnerOrReadOnly
from apps.utils.viewsets import RetrieveUpdateDestroyViewSet

from .models import Comment, Like, Post
from .serializers.comments import CommentSerializer
from .serializers.likes import LikeSerializer
from .serializers.posts import (
    ReadPostSerializer,
    WritePostSerializer,
)


class FeedViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = ReadPostSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ("$content",)

    def get_queryset(self):
        user = self.request.user

        return Post.objects.filter(Q(user__followers__from_user=user) | Q(user=user))


class PostViewSet(RetrieveUpdateDestroyViewSet):
    queryset = Post.objects.all()
    permission_classes = (IsOwnerOrReadOnly,)

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return ReadPostSerializer

        if self.action == "comments":
            return CommentSerializer

        return WritePostSerializer

    @action(detail=True, methods=["GET", "POST"], permission_classes=[])
    def comments(self, request, pk=None):
        post = self.get_object()

        if request.method == "GET":
            comments = Comment.objects.filter(post=post)

            page = self.paginate_queryset(comments)

            if page is not None:
                serializer = CommentSerializer(
                    page,
                    many=True,
                    context={"request": request},
                )

                return self.get_paginated_response(serializer.data)

            serializer = CommentSerializer(
                comments,
                many=True,
                context={"request": request},
            )

            return Response(serializer.data, status=status.HTTP_200_OK)

        elif request.method == "POST":
            serializer = CommentSerializer(
                data=request.data,
                context={"request": request},
            )

            serializer.is_valid(raise_exception=True)

            serializer.save(user=request.user, post=post)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["GET"], permission_classes=[])
    def likes(self, request, pk=None):
        post = self.get_object()

        likes = Like.objects.filter(post=post)

        page = self.paginate_queryset(likes)

        if page is not None:
            serializer = LikeSerializer(
                page,
                many=True,
                context={"request": request},
            )

            return self.get_paginated_response(serializer.data)

        serializer = LikeSerializer(
            likes,
            many=True,
            context={"request": request},
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["POST"], permission_classes=[])
    def like_post(self, request, pk=None):
        post = self.get_object()

        like, created = Like.objects.get_or_create(user=request.user, post=post)

        if created:
            return Response(
                data={"detail": "Post liked successfully."},
                status=status.HTTP_201_CREATED,
            )

        return Response(
            data={"detail": "Post already liked."}, status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=True, methods=["DELETE"], permission_classes=[])
    def unlike_post(self, request, pk=None):
        post = self.get_object()

        try:
            like = Like.objects.get(user=request.user, post=post)
        except Like.DoesNotExist:
            return Response(
                data={"detail": "Post not liked."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        like.delete()

        return Response(
            data={"detail": "Post unliked successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )


class CommentViewSet(RetrieveUpdateDestroyViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsOwnerOrReadOnly,)
