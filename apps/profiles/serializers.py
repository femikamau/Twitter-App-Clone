from rest_framework import serializers
from rest_framework.reverse import reverse

from apps.friends.models import Friend
from apps.posts.models import Post

from .models import Profile


class ListProfileSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    username = serializers.StringRelatedField(read_only=True, source="user")

    class Meta:
        model = Profile
        fields = (
            "url",
            "username",
            "avatar",
            "bio",
        )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["followers"] = Friend.objects.filter(
            to_user=instance.user
        ).count()
        representation["following"] = Friend.objects.filter(
            from_user=instance.user
        ).count()

        return representation

    def get_url(self, obj):
        return reverse(
            viewname="profile-detail",
            args=[obj.user.username],
            request=self.context.get("request"),
        )


class RetrieveProfileSerializer(ListProfileSerializer):
    class Meta(ListProfileSerializer.Meta):
        pass

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["posts"] = Post.objects.filter(user=instance.user).count()

        return representation
