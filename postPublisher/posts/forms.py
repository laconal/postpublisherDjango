from django.forms import ModelForm
from .models import Post

class PostCreate(ModelForm):
    class Meta:
        model = Post
        fields = ["title", "body"]