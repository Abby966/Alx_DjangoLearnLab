# blog/forms.py
from django import forms
from .models import Post
from taggit.forms import TagWidget   # ← import this

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content", "tags"]
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Post title"}),
            "content": forms.Textarea(attrs={"rows": 8, "placeholder": "Write your post..."}),
            "tags": TagWidget(),   # ← this makes the assignment happy
        }
