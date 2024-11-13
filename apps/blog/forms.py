from django import forms

from apps.users.models import User, UserProfile
from .models import Post


default_attrs = lambda name, placeholder: { # noqa :E731
    "name": name,
    "placeholder": placeholder,
    "class": "form-control",
}


class PostCreateUpdateForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ("title", "description", "content", "status")

        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "name": "title",
                    "placeholder": "Enter you`r post title...",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "name": "description",
                    "placeholder": "Enter you`r post description...",
                }
            ),
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "name": "content",
                    "placeholder": "Enter you`r post content...",
                }
            ),
            "status": forms.Select(
                attrs={
                    "class": "form-select",
                    "name": "status",
                    "placeholder": "Enter you`r post status...",
                }
            ),
        }


class SettingsUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email")

    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs=default_attrs("first_name", "First name..."),
        ),
        required=False,
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs=default_attrs("last_name", "Last name"),
        ),
        required=False,
    )
    username = forms.CharField(
        widget=forms.TextInput(
            attrs=default_attrs("username", "Username..."),
        )
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs=default_attrs("email", "Email..."))
    )


class SettingsUserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ("avatar", "bio")

    avatar = forms.ImageField(
        widget=forms.FileInput(attrs=default_attrs("avatar", "Avatar..."))
    )
    bio = forms.CharField(widget=forms.TextInput(attrs=default_attrs("bio", "Bio...")))
