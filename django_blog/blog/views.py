# blog/views.py
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Post
from .forms import PostForm
from .forms import RegisterForm, ProfileForm  # if you created these in the auth task

# -------- Blog Post CRUD --------

class PostListView(ListView):
    """
    Shows all posts (newest first thanks to Post.Meta.ordering).
    URL: /posts/   (also used for homepage "")
    """
    model = Post
    template_name = "blog/posts_list.html"
    context_object_name = "posts"
    paginate_by = 10  # optional

class PostDetailView(DetailView):
    """
    Shows a single post.
    URL: /posts/<pk>/
    """
    model = Post
    template_name = "blog/posts_detail.html"
    context_object_name = "post"

class PostCreateView(LoginRequiredMixin, CreateView):
    """
    Create a new post (auth required).
    URL: /posts/new/
    """
    model = Post
    form_class = PostForm
    template_name = "blog/posts_form.html"
    success_url = reverse_lazy("post-list")

    def form_valid(self, form):
        # Attach the logged-in user as author
        form.instance.author = self.request.user
        messages.success(self.request, "Post created.")
        return super().form_valid(form)

class AuthorRequiredMixin(UserPassesTestMixin):
    """
    Only the post's author can edit or delete.
    """
    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user

class PostUpdateView(LoginRequiredMixin, AuthorRequiredMixin, UpdateView):
    """
    Edit a post (only by author).
    URL: /posts/<pk>/edit/
    """
    model = Post
    form_class = PostForm
    template_name = "blog/posts_form.html"

    def get_success_url(self):
        messages.success(self.request, "Post updated.")
        return reverse_lazy("post-detail", kwargs={"pk": self.object.pk})

class PostDeleteView(LoginRequiredMixin, AuthorRequiredMixin, DeleteView):
    """
    Delete a post (only by author).
    URL: /posts/<pk>/delete/
    """
    model = Post
    template_name = "blog/posts_confirm_delete.html"
    success_url = reverse_lazy("post-list")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Post deleted.")
        return super().delete(request, *args, **kwargs)

# -------- Optional homepage: reuse the ListView --------
# (django_blog/urls.py maps "" to blog.urls; see urls below)

# -------- Auth views you added earlier (keep these if you have them) --------
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created! You can log in now.")
            return redirect("login")
    else:
        form = RegisterForm()
    return render(request, "blog/register.html", {"form": form})

@login_required
def profile(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated.")
            return redirect("profile")
    else:
        form = ProfileForm(instance=request.user)
    return render(request, "blog/profile.html", {"form": form})
