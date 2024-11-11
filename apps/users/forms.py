from django.core.exceptions import ValidationError
from django import forms

from .models import User


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(
            attrs={"placeholder": "Username...", "class": "form-control rounded-4"}
        ),
        error_messages={
            "required": "Username is required!",
            'max_length': "Username is too lang, max length is 150 charecters."
        }
    )
    password = forms.CharField(
        max_length=60,
        widget=forms.PasswordInput(
            attrs={"placeholder": "Password...", "class": "form-control rounded-4"}
        ),
        error_messages={
            "required": "Password is required!",
            "max_length": "Password is to long, max length is 60 charecters."
        }
    )


class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Password",
        max_length=28,
        widget=forms.PasswordInput(attrs={"id": "password", "type": "password"}),

    )
    password2 = forms.CharField(
        label="Password (Confirm)",
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
            return ValidationError("Passwords must be match!")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})

    class Meta:
        model = User
        fields = (
            "username",
            "password1",
            "password2",
            "email",
        )
