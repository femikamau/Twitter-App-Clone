from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # API (V1) Endpoints
    path(route="api/v1/", view=include("apis.v1.urls")),
    # Admin Site
    path("admin/", admin.site.urls),
]
