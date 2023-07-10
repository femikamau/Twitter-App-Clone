from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from apps.accounts.views import AccountViewSet
from apps.auth.views import RegisterAccountAPIView, logout_user
from apps.posts.views import CommentViewSet, FeedViewSet, PostViewSet
from apps.profiles.views import ProfileViewSet

router = DefaultRouter()

router.register(r"accounts", AccountViewSet, basename="account")
router.register(r"profiles", ProfileViewSet, basename="profile")
router.register(r"posts", PostViewSet, basename="post")
router.register(r"comments", CommentViewSet, basename="comment")
router.register(r"feed", viewset=FeedViewSet, basename="feed")

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
        route="logout/",
        view=logout_user,
        name="logout",
    ),
    path(
        route="rest-auth/",
        view=include("rest_framework.urls"),
    ),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    # Optional UI:
    path(
        "schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
] + router.urls
