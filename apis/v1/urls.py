from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from apps.accounts.views import AccountViewSet
from apps.auth.views import RegisterAccountAPIView
from apps.friends.views import FollowerViewSet, FollowingViewSet
from apps.posts.views import CommentViewSet, PostViewSet
from apps.profiles.views import ProfileViewSet

router = DefaultRouter()

router.register(r"accounts", AccountViewSet, basename="account")
router.register(r"profiles", ProfileViewSet, basename="profile")
router.register(r"posts", PostViewSet, basename="post")
router.register(r"comments", CommentViewSet, basename="comment")
router.register(r"following", FollowingViewSet, basename="following")
router.register(r"followers", FollowerViewSet, basename="follower")


urlpatterns = [
    path(
        route="register/",
        view=RegisterAccountAPIView.as_view(),
        name="register",
    ),
    path(
        route="login/",
        view=obtain_auth_token,
        name="login",
    ),
    path(
        route="rest-auth/",
        view=include("rest_framework.urls"),
    ),
] + router.urls
