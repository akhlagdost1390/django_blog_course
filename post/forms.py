from django import forms
from .models import Post
from django.utils.text import slugify
from django.contrib.auth.models import User


class NewPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "banner", "tags", "body", "published", "category"]
        field_classes = {
            "banner": forms.ImageField,
        }
        widgets = {
            "title": forms.TextInput(attrs={"class": "block input"}),
            "banner": forms.FileInput(attrs={"class": "block"}),
            "tags": forms.TextInput(attrs={"class": "block input"}),
            "published": forms.CheckboxInput(attrs={"class": "block"}),
            "category": forms.Select(attrs={"class": "block input"}),
            "body": forms.Textarea(attrs={"class": "block input"}),
        }

    def save(self, commit: bool = True, user: User = None):
        if user is None:
            raise User.DoesNotExist()

        post: Post = super().save(commit=False)
        title = post.title
        slug = slugify(title)
        post.slug = slug
        post.user = user

        if commit:
            post.save()
        return post


class EditPostForm(NewPostForm):
    pass
