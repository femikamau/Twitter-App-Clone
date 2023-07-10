from django.contrib.auth import logout
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from apps.accounts.models import User

from .permissions import IsNotAuthenticated
from .serializers import RegisterAccountSerializer


class RegisterAccountAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterAccountSerializer
    permission_classes = (IsNotAuthenticated,)


@api_view(["DELETE"])
@permission_classes([permissions.IsAuthenticated])
def logout_user(request):
    request.user.auth_token.delete()

    logout(request)

    return Response(
        data={"message": "You have been successfully logged out."},
        status=status.HTTP_204_NO_CONTENT,
    )
