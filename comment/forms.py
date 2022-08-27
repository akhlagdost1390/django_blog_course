from django import forms
from .models import Comment
from django.contrib.auth.models import User
from post.models import Post

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        widgets = {
            'body': forms.Textarea(attrs={'class': 'textarea is-small ta'})
        }
        labels = {
            'body': ''
        }
    def save(self, commit: bool, user:User, post:Post):
        comment: Comment =  super().save(commit=False)
        comment.user = user
        comment.post = post

        if commit:
            comment.save()
        return Comment