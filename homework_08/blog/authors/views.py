from django.shortcuts import render
from authors.models import Post, Authors

from django.views.generic import ListView, DetailView


def index(request):
    return render(request, 'authors/index.html')


class AuthorsListView(ListView):
    model = Authors


class PostsListView(ListView):
    model = Post
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.select_related('name').all()
        return qs


class PostDetailView(DetailView):
    model = Post

