from rest_framework import serializers

from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="profile-detail",
        read_only=True,
    )
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Profile
        fields = (
            "id",
            "url",
            "user",
            "bio",
            "avatar",
        )
