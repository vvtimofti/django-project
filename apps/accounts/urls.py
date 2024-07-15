from django.shortcuts import redirect
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from . import views


urlpatterns = [
    path("accounts/", lambda req: redirect("login/")),
    path("accounts/signup/", views.SignUpView.as_view(), name="signup"),
    path("accounts/logout/", views.logout_view, name="logout"),
    path("accounts/login/", views.LoginViewCustom.as_view(), name="login"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("@<str:username>/follow/", views.toggle_follow, name="toggle_follow"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

htmx_urlpatterns = [
    path("check-username/", views.check_username, name="check-username"),
    path("check-password/", views.check_password, name="check-password"),
]

urlpatterns += htmx_urlpatterns