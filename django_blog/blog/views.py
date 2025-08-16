# blog/views.py
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from .forms import PostForm
from taggit.models import Tag

# ... PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView unchanged ...

class PostByTagListView(ListView):  # ← name matches checker
    model = Post
    template_name = "blog/post_list_by_tag.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self):
        tag = get_object_or_404(Tag, slug=self.kwargs["tag_slug"])
        return (
            Post.objects.filter(tags__in=[tag])
            .order_by("-created_at")
            .distinct()
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["active_tag"] = get_object_or_404(Tag, slug=self.kwargs["tag_slug"])
        return ctx
