from django import forms
from .models import User, Post
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=28,
        widget=forms.TextInput(
            attrs={"placeholder": "Username...", "class": "form-control rounded-4"}
        ),
    )
    password = forms.CharField(
        max_length=60,
        widget=forms.PasswordInput(
            attrs={"placeholder": "Password...", "class": "form-control rounded-4"}
        ),
    )


class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(
        max_length=28,
        widget=forms.PasswordInput(attrs={"id": "password", "type": "password"}),
    )
    password2 = forms.CharField(
        max_length=28,
        widget=forms.PasswordInput(attrs={"id": "password", "type": "password"}),
    )

    def save(self, commit=True):
        user = super().save(commit)

        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 == password2:
            user.set_password(password1)
            user.save()
        else:
            raise ValidationError("Password must be match")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "password1",
            "password2",
            "email",
            "avatar",
        )


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
        }


class PostUpdateForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ("title", "content", "is_active")
