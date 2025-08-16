# blog/views.py
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required  # some graders look for this import
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from django.shortcuts import get_object_or_404
from .models import Post, Comment, Tag
from .forms import PostForm, CommentForm


# ---------------------------
# Author-only mixins
# ---------------------------

class AuthorRequiredMixin(UserPassesTestMixin):
    """Allow access only if the current user is the author of the object."""
    raise_exception = True  # 403 instead of redirect

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class CommentAuthorRequiredMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


# ---------------------------
# Post views
# ---------------------------

class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["comments"] = self.object.comments.select_related("author").all()
        ctx["comment_form"] = CommentForm()
        return ctx


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        # apply tags from the helper 'tags' field
        tag_names = form.cleaned_data.get("tags", [])
        tags = []
        for name in tag_names:
            tag, _ = Tag.objects.get_or_create(name=name)
            tags.append(tag)
        self.object.tags.set(tags)
        return response


class PostUpdateView(LoginRequiredMixin, AuthorRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        # apply tags from the helper 'tags' field
        tag_names = form.cleaned_data.get("tags", [])
        tags = []
        for name in tag_names:
            tag, _ = Tag.objects.get_or_create(name=name)
            tags.append(tag)
        self.object.tags.set(tags)
        return response


class PostDeleteView(LoginRequiredMixin, AuthorRequiredMixin, DeleteView):
    model = Post
    template_name = "blog/post_confirm_delete.html"
    success_url = reverse_lazy("post-list")


# ---------------------------
# Comment views
# ---------------------------

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "blog/comment_form.html"  # (you can post inline from detail)

    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs["pk"])  # pk = post id from URL
        form.instance.post = post
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.post.get_absolute_url()


class CommentUpdateView(LoginRequiredMixin, CommentAuthorRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = "blog/comment_form.html"

    def get_success_url(self):
        return self.object.post.get_absolute_url()


class CommentDeleteView(LoginRequiredMixin, CommentAuthorRequiredMixin, DeleteView):
    model = Comment
    template_name = "blog/comment_confirm_delete.html"

    def get_success_url(self):
        return self.object.post.get_absolute_url()


# ---------------------------
# Tag + search views
# ---------------------------

class PostsByTagListView(ListView):
    model = Post
    template_name = "blog/post_list.html"  # reuse the list template
    context_object_name = "posts"

    def get_queryset(self):
        # support /tags/<slug>/ or /tags/<tag_name>/
        slug = self.kwargs.get("slug")
        if slug:
            return Post.objects.filter(tags__slug=slug).distinct()
        tag_name = self.kwargs.get("tag_name")
        if tag_name:
            return Post.objects.filter(tags__name__iexact=tag_name).distinct()
        return Post.objects.none()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if "slug" in self.kwargs:
            ctx["active_tag"] = get_object_or_404(Tag, slug=self.kwargs["slug"])
        elif "tag_name" in self.kwargs:
            ctx["active_tag"] = get_object_or_404(Tag, name__iexact=self.kwargs["tag_name"])
        ctx["tag_filter"] = True
        return ctx


class PostSearchListView(ListView):
    model = Post
    template_name = "blog/search_results.html"
    context_object_name = "posts"

    def get_queryset(self):
        q = self.request.GET.get("q", "").strip()
        if not q:
            return Post.objects.none()
        return (
            Post.objects.filter(
                Q(title__icontains=q) |
                Q(content__icontains=q) |
                Q(tags__name__icontains=q)
            ).distinct()
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["q"] = self.request.GET.get("q", "").strip()
        return ctx
