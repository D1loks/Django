from django.db.models import Q
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic import DetailView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from .models import BlogPost
from django.http import Http404
from .ownerviews import *


class BlogListView(ListView):
    model = BlogPost
    paginate_by = 2

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return BlogPost.objects.filter(
                Q(status='public') | Q(owner=self.request.user)
            )
        else:
            return BlogPost.objects.filter(status='public')


class BlogDetailView(DetailView):
    model = BlogPost

    def get_object(self, queryset=None):
        pk = self.kwargs.get("pk")
        year = self.kwargs.get("year")
        month = self.kwargs.get("month")
        day = self.kwargs.get("day")
        slug_id = self.kwargs.get("slug_id")

        if pk:
            obj = get_object_or_404(self.model, pk=pk)
        elif slug_id:
            obj = get_object_or_404(
                self.model,
                created_at__year=year,
                created_at__month=month,
                created_at__day=day,
                slug=slug_id
            )
        else:
            raise Http404("No object found matching the provided criteria.")

        if obj.status == 'draft' and obj.owner != self.request.user:
            raise Http404("You do not have permission to view this post.")

        return obj


class BlogDeleteView(OwnerDeleteView):
    model = BlogPost
    success_url = reverse_lazy("blog_app:posts")


class BlogPostCreateView(OwnerCreateView):
    model = BlogPost
    fields = ["title", "text", "status"]
    success_url = reverse_lazy("blog_app:posts")


class BlogUpdateView(OwnerUpdateView):
    model = BlogPost
    fields = ["title", "text", "status"]
    success_url = reverse_lazy("blog_app:posts")

