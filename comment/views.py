from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse
from .forms import CommentForm
from post.models import Post
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def send(request: HttpRequest):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            post_id = request.POST.get("post_id")
            post = get_object_or_404(Post.available_posts, id=int(post_id))
            form.save(commit=True, user=request.user, post=post)
            return redirect(post.get_absolute_url())
    else:
        form = CommentForm()
