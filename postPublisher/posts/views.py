from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Q
from . import models
from . import forms
# Create your views here.

User = get_user_model()

def listView(request):
    if request.method == "GET":
        q = request.GET.get("q") if request.GET.get("q") != None else ""
        posts = models.Post.objects.filter(
            Q(title__icontains = q) |
            Q(createdBy__username__icontains = q) |
            Q(body__icontains = q)
            )
        return render(request, "list.html", {"posts": posts})
    posts = models.Post.objects.all()
    return render(request, 'list.html', {'posts': posts})

@login_required(login_url = "users:login")
def addPost(request):
    if request.method == "POST":
        post = models.Post(title = request.POST["title"],
                           body = request.POST["body"],
                           createdBy = request.user)
        post.save()
        return listView(request)
    return render(request, "addPost.html")

def viewPost(request, postID):
    post = get_object_or_404(models.Post, id = postID)
    return render(request, "post.html", {"post": post})

@login_required(login_url = "users:login")
def likePost(request, postID):
    post = get_object_or_404(models.Post, id = postID)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
        post.dislikes.remove(request.user)
    nextURL = request.GET.get("next", "list.html")
    return HttpResponseRedirect(nextURL)

@login_required(login_url = "users:login")
def dislikePost(request, postID):
    post = get_object_or_404(models.Post, id = postID)
    if request.user in post.dislikes.all():
        post.dislikes.remove(request.user)
    else:
        post.dislikes.add(request.user)
        post.likes.remove(request.user)
    nextURL = request.GET.get("next", "list.html")
    return HttpResponseRedirect(nextURL)

@login_required(login_url = "users:login")
def leaveComment(request, postID):
    post = get_object_or_404(models.Post, id = postID)
    if request.method == "POST":
        commentText = request.POST.get("commentText")
        if commentText:
            comment = models.Comment.objects.create(
                body = commentText,
                post = post,
                author = request.user
            )
            post.comments.add(comment)
        return viewPost(request, postID)

def editPost(request, postID):
    if request.method == "POST":
        post = get_object_or_404(models.Post, id = postID)
        post.title = request.POST.get("title")
        post.body = request.POST.get("body")
        post.save()
        return redirect("users:userProfile")
    else:
        post = get_object_or_404(models.Post, id = postID)
        return render(request, "editPost.html", {"post": post})

def replyComment(request, commentID):
    if request.method == "POST":
        initialComment = get_object_or_404(models.Comment, id = commentID)
        replyComment = models.Comment.objects.create(
            body = request.POST["commentText"],
            author = request.user,
            post = initialComment.post
        )
        initialComment.subComments.add(replyComment)
        initialComment.save()
        return viewPost(request, initialComment.post.id)