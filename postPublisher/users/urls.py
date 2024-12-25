from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("register/", views.registerView, name = "userRegistration"),
    path("logout/", views.logoutView, name = "logout"),
    path("login/", views.loginView, name = "login"),
    path("myProfile/", views.userProfile, name = "userProfile"),
    path("deletePost/<int:postID>/", views.deletePost, name = "deletePost"),
    path("addToBookmarks/<int:postID>", views.addToBookmarks, name = "addToBookmarks"),
    path("myBookmarks", views.bookmarksView, name = "bookmarksView"),
    path("deleteFromBookmarks/<int:postID>", views.deleteFromBookmarks, name = "deleteFromBookmarks")
]