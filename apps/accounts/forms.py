from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from apps.accounts.models import Profile


class UserCreateForm(UserCreationForm):
    username = forms.CharField(max_length=10, min_length=3, required=True)
    display_name = forms.CharField(max_length=20, min_length=3, required=True)

    class Meta:
        fields = ("username", "display_name", "password1", "password2")
        model = get_user_model()

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.display_name = self.cleaned_data["display_name"]
        if commit:
            user.save()
        return user


class ProfileForm(forms.ModelForm):
    display_name = forms.CharField(max_length=20, min_length=3)

    class Meta:
        model = Profile
        fields = ['display_name', 'profile_picture', 'bio']
