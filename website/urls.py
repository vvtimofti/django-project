from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("post/", include("apps.posts.urls")),
    path("", include("apps.core.urls")),
    path("", include("apps.chat.urls")),
    path("", include("apps.accounts.urls")),
]
