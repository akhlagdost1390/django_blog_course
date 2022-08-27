from django.shortcuts import render, redirect
from .forms import UserRegisterForm, ProfileRegisterForm, EditProfileForm, EditUserForm, ThemeForm
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.messages import add_message, SUCCESS, ERROR
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_GET
from comment.models import Comment

# Create your views here.

def register(request: HttpRequest):
    if request.method == "POST":
        u_form = UserRegisterForm(request.POST)
        p_form = ProfileRegisterForm(data=request.POST, files=request.FILES)
        
        if u_form.is_valid() and p_form.is_valid():
            new_user: User = u_form.save(commit=True)
            user_profile: Profile = p_form.save(commit=False)
            user_profile.user = new_user
            user_profile.save()
            
            add_message(
                request,
                SUCCESS,
                "We are glad that you joined us, now you can log in",
                'notification is-success is-light',
                True
            )
            return  redirect('login')
    else:
        u_form = UserRegisterForm()
        p_form = ProfileRegisterForm()
        
    return render(request, "registration/register.html", {'u_form': u_form, 'p_form': p_form})

@login_required
def dashboard(request: HttpRequest):
    posts = request.user.posts.all()
    liked_post = request.user.likes.all()
    comments = request.user.user_comments.all()
    print(comments)
    theme_form = ThemeForm(instance=request.user.profile)
    return render(request, "account/dashboard.html", {'t_form': theme_form, 'posts': posts, 'liked_post': liked_post})

@login_required
@require_GET
def change_theme(request: HttpRequest):
    if request.method == "GET":
        form = ThemeForm(data = request.GET, instance=request.user.profile)
        if form.is_valid():
            profile: Profile = request.user.profile
            profile.theme = form.cleaned_data.get("theme")
            profile.save()
            return redirect("dashboard")
    return redirect("dashboard")
        

@login_required
def edit_info(request: HttpRequest):
    if request.method == "POST":
        u_form = EditUserForm(data=request.POST, instance=request.user)
        p_form = EditProfileForm(data=request.POST, files=request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            
            user: User = u_form.save(commit=False)
            user.username = user.email
            user.save()
            profile = p_form.save()
            add_message(request, SUCCESS, "Your Info Updated SuccessFully.", "notification is-success", True)
            return redirect("dashboard")
        
        else:
            return HttpResponse(f"{u_form.errors} {p_form.errors}")
    else:
        u_form = EditUserForm(instance=request.user)
        p_form = EditProfileForm(instance=request.user.profile)
    return render(request, 'account/edit_info.html', {'u_form': u_form, 'p_form': p_form})