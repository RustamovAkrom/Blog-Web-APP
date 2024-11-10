from django import forms
from .models import Post


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
