# blog/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Comment,Tag

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content"]
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Post title"}),
            "content": forms.Textarea(attrs={"rows": 8, "placeholder": "Write your post..."}),
        }

class RegisterForm(UserCreationForm):
    """Extend Django's registration form to capture email."""
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class ProfileForm(forms.ModelForm):
    """Simple profile editor for core User fields."""
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(attrs={"rows": 3, "placeholder": "Write a comment…"})
        }
class PostForm(forms.ModelForm):
    # Users type:  django, web, tutorial
    tags_input = forms.CharField(
        required=False,
        help_text="Comma-separated tags, e.g. django, web, tutorial"
    )

    class Meta:
        model = Post
        fields = ["title", "content", "tags_input"]  # tags set from tags_input

    def __init__(self, *args, **kwargs):
        # Pre-fill tags_input when editing
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            current = ", ".join(self.instance.tags.values_list("name", flat=True))
            self.fields["tags_input"].initial = current

    def clean_tags_input(self):
        raw = self.cleaned_data.get("tags_input", "")
        # Normalize: split by comma, strip spaces, remove empties, lowercase
        parts = [p.strip() for p in raw.split(",") if p.strip()]
        # Deduplicate while keeping order
        seen, out = set(), []
        for p in parts:
            low = p.lower()
            if low not in seen:
                seen.add(low)
                out.append(p)
        return out  # list of tag names
