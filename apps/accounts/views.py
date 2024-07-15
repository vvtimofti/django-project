from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import logout, get_user_model, login
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.password_validation import validate_password

from . import forms
from .models import Profile


def check_username(request):
    username = request.POST.get("username")
    if get_user_model().objects.filter(username=username).exists():
        return HttpResponse("<p style='color: red'>This username is taken!</p>")
    elif not username:
        return HttpResponse("<p style='color: red'>Username field cannot be empty!</p>")
    elif " " in username:
        return HttpResponse("<p style='color: red'>Username cannot contain spaces!</p>")

    return HttpResponse("<p style='color: green'>This username is available.</p>")


def check_password(request):
    password = request.POST.get("password1")
    confirm_password = request.POST.get("password2")

    try:
        validate_password(password)
        if password != confirm_password:
            return HttpResponse("<p style='color: red'>Passwords do not match!</p>")
    except Exception as e:
        error_messages = ""
        for error in e:
            error_messages += f"<p style='color: red'>{error}</p>"
        return HttpResponse(f"<p style='color: red'>{error_messages}</p>")

    return HttpResponse("<p style='color: green'>Passwords match.</p>")


@login_required
def toggle_follow(request, username):
    profile = request.user.profile
    follow_profile = get_object_or_404(User, username=username).profile

    if follow_profile not in profile.following.all():
        profile.following.add(follow_profile)
    else:
        profile.following.remove(follow_profile)

    return render(request, "posts/partials/follow_section.html", {"profile": follow_profile, "username": username})


class SignUpView(CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy("home")
    template_name = "accounts/signup.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        Profile.objects.create(
            user=self.object, display_name=self.object.display_name)
        login(self.request, self.object)
        return response

    def get_context_data(self, **kwargs) -> dict[str]:
        context = super().get_context_data(**kwargs)
        if self.request.htmx:
            context["base_template"] = "_join.html"
        else:
            context["base_template"] = "_base.html"
        context["page_title"] = "Sign Up"
        return context


class LoginViewCustom(LoginView):
    template_name = "accounts/login.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs) -> dict[str]:
        context = super().get_context_data(**kwargs)
        if self.request.htmx:
            context["base_template"] = "_join.html"
        else:
            context["base_template"] = "_base.html"
        context["page_title"] = "Sign In"
        return context


def logout_view(request):
    logout(request)
    return redirect("/")
