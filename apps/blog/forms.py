from django import forms

from apps.users.models import User, UserProfile
from .models import Post


default_attrs = lambda name, placeholder: {
    "name": name,
    "placeholder": placeholder,
    "class": "form-control"
}

class PostCreateForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ["title", "content", "is_active"]

        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter you`r post title...",
                }
            ),
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter you`r post content...",
                }
            ),
            "is_active": forms.CheckboxInput(
                attrs={
                    "name": "is_active",
                    "class": "form-check-input"
                }
            )
        }


class PostUpdateForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ("title", "content", "is_active")

        widgets = {
            "title": forms.TextInput(
                attrs={
                    "name": "title",
                    "class": "form-control",
                    "placeholder": "Title...."
                },
            ),
            "content": forms.Textarea(
                attrs={
                    "name": "content",
                    "cols": "40",
                    "rows": "10",
                    "class": "form-control",
                    "placeholder": "Content...."
                },
            ),
            "is_active": forms.CheckboxInput(
                attrs={
                    "name": "is_active",
                    "class": "form-check-input"
                }
            )
        }


class SettingsForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(
        attrs=default_attrs("first_name", "First name..."),
    ))
    last_name = forms.CharField(widget=forms.TextInput(
        attrs=default_attrs("last_name", "Last name"),
    ))
    username = forms.CharField(widget=forms.TextInput(
        attrs=default_attrs("username", "Username..."),
    ))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs=default_attrs("email", "Email...")
    ))
    avatar = forms.ImageField(widget=forms.FileInput(
        attrs=default_attrs("avatar", "Avatar...")
    ))
    bio = forms.CharField(widget=forms.TextInput(
        attrs=default_attrs("bio", "Bio...")
    ))
