from rest_framework import serializers
from rest_framework.reverse import reverse

from ..models import Post


class WritePostSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="post-detail", read_only=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Post
        fields = (
            "url",
            "user",
            "content",
            "image",
            "created_at",
            "updated_at",
        )


class ReadPostSerializer(WritePostSerializer):
    user = serializers.SerializerMethodField()

    class Meta(WritePostSerializer.Meta):
        pass

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        representation["comments"] = instance.comments.count()

        return representation

    def get_user(self, obj):
        return reverse(
            viewname="profile-detail",
            args=[obj.user.username],
            request=self.context.get("request"),
        )
