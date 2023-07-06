from rest_framework import serializers

from .models import User


class AccountSerializer(serializers.ModelSerializer):
    """
    User Serializer
    """

    url = serializers.HyperlinkedIdentityField(view_name="account-detail")

    class Meta:
        model = User
        fields = (
            "id",
            "url",
            "email",
            "first_name",
            "last_name",
            "is_active",
            "is_staff",
        )
