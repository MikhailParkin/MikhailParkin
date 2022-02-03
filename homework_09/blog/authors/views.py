from django.db.models import Count
from django.shortcuts import render
from authors.models import Post

from myauth.models import MyUser

from django.views.generic import ListView, DetailView


def index(request):
    return render(request, 'authors/index.html')


class PostsListView(ListView):
    model = Post
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.select_related('name').all()
        return qs


class PostDetailView(DetailView):
    model = Post


class AuthorsListView(ListView):
    model = MyUser
    template_name = 'authors/author_list.html'

    def get_queryset(self):
        qs = super().get_queryset()
        # qs = qs.values('name_id').annotate(dcount=Count('name_id')).order_by('name_id')
        # qs = qs.filter('first_name', 'last_name').order_by('name_id')
        # qs = qs.select_related('name').all()
        print(qs)
        return qs


