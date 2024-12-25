from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()

class Post(models.Model):
    title = models.CharField(max_length = 25, verbose_name = 'Title')
    body = models.CharField(max_length = 25, verbose_name = 'Body')
    createdBy = models.ForeignKey(User, on_delete = models.DO_NOTHING)
    createdTime = models.DateTimeField(auto_now_add = True, verbose_name = 'Created time')
    likes = models.ManyToManyField(User, related_name = "likedPosts", blank = True)
    dislikes = models.ManyToManyField(User, related_name = "dislikedPosts", blank = True)
    comments = models.ManyToManyField("Comment", related_name = "comments", blank = True)

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    body = models.TextField()
    post = models.ForeignKey(Post, blank = True, on_delete = models.CASCADE)
    author = models.ForeignKey(User, blank = True, on_delete = models.DO_NOTHING)
    liked = models.IntegerField(default = 0)
    disliked = models.IntegerField(default = 0)
    date = models.DateTimeField(auto_now_add = True)
    subComments = models.ManyToManyField("self", blank = True, symmetrical = False)
    
    def __str__(self):
        return self.body[0:25]
