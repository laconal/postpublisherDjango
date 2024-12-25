from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from posts.models import Post
from django.contrib.auth import get_user_model
from .forms import CustomUserCreationForm
# Create your views here.


def registerView(request):
    if request.method == "POST":
        # form = UserCreationForm(request.POST)
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("posts:list")
    else: form = CustomUserCreationForm()
    return render(request, 'registration.html', {"form": form})

def loginView(request):
    form = None
    if request.method == "POST":
        user = authenticate(request, username = request.POST["username"],
                            password = request.POST["password"])
        if user is not None:
            login(request, user)
            if "next" in request.POST:
                return redirect(request.POST.get("next"))
            return redirect("posts:list")
    else: form = AuthenticationForm()
    return render(request, "login.html", {"form": form})

def logoutView(request):
    if request.method == "POST":
        logout(request)
        return redirect("posts:list")

@login_required(login_url = "users:login")
def userProfile(request):
    posts = Post.objects.filter(createdBy = request.user)
    return render(request, "userProfile.html",
                  {"username": request.user.username,
                   "posts": posts})

@login_required(login_url = "users:login")
def deletePost(request, postID):
    if request.method == "POST":
        post = get_object_or_404(Post, id = postID)
        if post.createdBy == request.user:
            post.delete()
            if "next" in request.POST:
                return redirect(request.POST.get("next"))
            return redirect("users:userProfile")
    return redirect("posts:list")

@login_required(login_url = "users:login")
def addToBookmarks(request, postID):
    if request.method == "POST":
        post = get_object_or_404(Post, id = postID)
        if request.user.bookmarks.filter(id = post.id).exists():
            request.user.bookmarks.remove(post)
        else:
            request.user.bookmarks.add(post)
    return redirect("posts:list")

def bookmarksView(request):
    posts = request.user.bookmarks.all()
    return render(request, "bookmarks.html",
                    {"posts": posts})
    
def deleteFromBookmarks(request, postID):
    if request.method == "POST":
        post = get_object_or_404(Post, id = postID)
        request.user.bookmarks.remove(post)
        nextURL = request.GET.get("next")
        if nextURL: return redirect(nextURL)
        else: return bookmarksView(request)