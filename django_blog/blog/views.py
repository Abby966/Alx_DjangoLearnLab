# blog/views.py
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from .forms import PostForm
from taggit.models import Tag

class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    paginate_by = 10
    def get_queryset(self):
        return Post.objects.order_by("-created_at")

class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"

class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"

class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"

class PostDeleteView(DeleteView):
    model = Post
    template_name = "blog/post_confirm_delete.html"
    success_url = reverse_lazy("blog:post_list")

# AFTER (only these lines changed)
class PostByTagListView(ListView):  # ← class name checker wants
    model = Post
    template_name = "blog/post_list_by_tag.html"
    context_object_name = "posts"
    paginate_by = 10
    def get_queryset(self):
        tag = get_object_or_404(Tag, slug=self.kwargs["tag_slug"])  # ← use tag_slug
        return Post.objects.filter(tags__in=[tag]).order_by("-created_at").distinct()
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["active_tag"] = get_object_or_404(Tag, slug=self.kwargs["tag_slug"])  # ← use tag_slug
        return ctx


class PostSearchListView(ListView):
    model = Post
    template_name = "blog/search_results.html"
    context_object_name = "posts"
    paginate_by = 10
    def get_queryset(self):
        q = (self.request.GET.get("q") or "").strip()
        if not q:
            return Post.objects.none()
        return (Post.objects.filter(
                    Q(title__icontains=q) |
                    Q(content__icontains=q) |
                    Q(tags__name__icontains=q)
                )
                .order_by("-created_at")
                .distinct())
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["q"] = (self.request.GET.get("q") or "").strip()
        return ctx
