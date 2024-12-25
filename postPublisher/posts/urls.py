from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.listView, name = "list"),
    path("addPost/", views.addPost, name = "addPost"),
    path("<int:postID>/", views.viewPost, name = "viewPost"),
    path("<int:postID>/likePost/", views.likePost, name = "likePost"),
    path("<int:postID>/dislikePost", views.dislikePost, name = "dislikePost"),
    path("<int:postID>/leaveComment", views.leaveComment, name = "leaveComment"),
    path("<int:postID>/edit", views.editPost, name = "editPost"),
    path("<int:commentID>/replyComment", views.replyComment, name = "replyComment")
]