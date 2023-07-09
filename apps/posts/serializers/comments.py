from rest_framework import serializers
from rest_framework.reverse import reverse

from ..models import Comment


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = (
            "url",
            "user",
            "post",
            "content",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("post", "user", "created_at", "updated_at")

    def get_user(self, obj):
        return reverse(
            viewname="profile-detail",
            args=[obj.user.username],
            request=self.context.get("request"),
        )
