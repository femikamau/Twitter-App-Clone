from rest_framework import serializers
from rest_framework.reverse import reverse

from ..models import Like


class LikeSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Like
        fields = (
            "id",
            "user",
            "created_at",
        )

    def get_user(self, obj):
        return reverse(
            viewname="profile-detail",
            args=[obj.user.username],
            request=self.context.get("request"),
        )
