from rest_framework import serializers

from .models import Comment, Post


class ReadPostSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="post-detail",
        read_only=True,
    )

    user = serializers.HyperlinkedRelatedField(
        view_name="account-detail",
        read_only=True,
    )

    class Meta:
        model = Post
        fields = (
            "id",
            "url",
            "user",
            "content",
            "image",
            "created_at",
            "updated_at",
        )


class WritePostSerializer(ReadPostSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Comment
        fields = (
            "id",
            "user",
            "post",
            "content",
            "created_at",
            "updated_at",
        )
