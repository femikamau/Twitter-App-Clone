from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers, validators

from apps.accounts.models import User


class RegisterAccountSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        validators=[validators.UniqueValidator(queryset=User.objects.all())],
    )

    email = serializers.EmailField(
        required=True,
        validators=[validators.UniqueValidator(queryset=User.objects.all())],
    )

    first_name = serializers.CharField(
        required=True,
    )

    last_name = serializers.CharField(
        required=True,
    )

    password1 = serializers.CharField(
        required=True,
        write_only=True,
        validators=[validate_password],
        label="Password",
    )

    password2 = serializers.CharField(
        required=True,
        write_only=True,
        label="Confirm Password",
    )

    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "username",
            "password1",
            "password2",
        )

    def validate(self, attrs):
        if attrs["password1"] != attrs["password2"]:
            raise serializers.ValidationError(
                detail={"password1": "Password fields didn't match"}
            )
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            password=validated_data["password1"],
        )

        return user
