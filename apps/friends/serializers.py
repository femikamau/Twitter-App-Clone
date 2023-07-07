from rest_framework import serializers

from .models import Friend


class FriendSerializer(serializers.ModelSerializer):
    from_user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Friend
        fields = (
            "id",
            "from_user",
            "to_user",
            "created_at",
        )

    def validate(self, data):
        if data["from_user"] == data["to_user"]:
            raise serializers.ValidationError("You can't follow yourself")

        if Friend.objects.filter(
            from_user=data["from_user"],
            to_user=data["to_user"],
        ).exists():
            raise serializers.ValidationError("You already follow this user")

        return data
