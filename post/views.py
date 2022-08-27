from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.urls import reverse
from .models import Post, Category
from django.core.paginator import Paginator, EmptyPage, InvalidPage, PageNotAnInteger
from tagging.models import Tag
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .forms import NewPostForm, EditPostForm
from django.contrib.messages import add_message, SUCCESS, ERROR
from comment.forms import CommentForm
from comment.models import Comment

# Create your views here.


def index(request: HttpRequest):
    categories = Category.objects.all()
    tags = Tag.objects.all()

    all_posts = Post.available_posts.all()
    paginator = Paginator(all_posts, 4)
    page = request.GET.get("page", 1)

    try:
        posts = paginator.page(page)
    except (InvalidPage, EmptyPage, PageNotAnInteger):
        posts = paginator.page(1)

    context = {"posts": posts, "categories": categories, "tags": tags}
    return render(request, "post/index.html", context)


def category_list(request: HttpRequest):
    categories = Category.objects.all()
    context = {"categories": categories}
    return render(request, "post/categories_list.html", context)


def category_posts(request: HttpRequest, slug):
    posts = Post.available_posts.filter(category__slug=slug)
    category_name = Category.objects.get(slug=slug)
    context = {"posts": posts, "category_name": category_name}
    return render(request, "post/category_posts.html", context)


def detail(request: HttpRequest, category=None, slug=None):
    comment_form = CommentForm()
    action = None
    post = get_object_or_404(Post, category__title=category, slug=slug)
    comments = Comment.objects.filter(post__id = post.id)
    ids = post.users_like.values_list('id', flat=True)
    if request.user.id in ids:
        action = 'dislike'
    else:
        action = 'like'

    context = {"post": post, 'action': action, 'form': comment_form, 'comments': comments}
    return render(request, "post/detail.html", context)


@login_required
def new_post(request: HttpRequest):
    if request.method == "POST":
        form = NewPostForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            post: Post = form.save(commit=True, user=request.user)
            add_message(
                request,
                SUCCESS,
                f"Post '{post.title}' added",
                "notification is-success",
                False,
            )
            return redirect("dashboard")
    else:
        form = NewPostForm()
    return render(request, "post/new_post.html", {"form": form})

def like(request: HttpRequest):
    if request.user.is_authenticated:
        if request.method == "POST":
            post_id = int(request.POST.get("post_id"))
            post = Post.available_posts.get(id=post_id)
            ids = request.user.likes.values_list("id", flat=True)

            if post_id in ids:
                post.users_like.remove(request.user)
                return JsonResponse(data={"action": "dislike"}, status=200)
            else:
                post.users_like.add(request.user)
                return JsonResponse(data={"action": "like"}, status=200)
    return JsonResponse(data={'action': 'login'}, status=403)



@login_required
def edit(request: HttpRequest, category, slug):
    post = Post.objects.get(category__title=category, slug=slug)
    if request.method == "POST":
        form = EditPostForm(instance=post, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save(commit=True, user=request.user)
            add_message(
                request,
                SUCCESS,
                f"Post '{post.title}' updated",
                "notification is-success",
                False,
            )
            return redirect("dashboard")
    else:
        form = EditPostForm(instance=post)
    return render(request, "post/edit_post.html", {"form": form})


def delete(request: HttpRequest, category, slug):
    post = get_object_or_404(Post, category__title=category, slug=slug)
    post.delete()
    add_message(
                request,
                ERROR,
                f"Post '{post.title}' Deleted",
                "notification is-danger",
                False,
            )
    return redirect('dashboard')