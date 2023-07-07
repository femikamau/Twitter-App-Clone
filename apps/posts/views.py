from rest_framework import viewsets

from apps.utils.permissions import IsAuthor

from .models import Comment, Post
from .serializers import (
    CommentSerializer,
    ReadPostSerializer,
    WritePostSerializer,
)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    permission_classes = (IsAuthor,)

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return WritePostSerializer
        return ReadPostSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthor,)
