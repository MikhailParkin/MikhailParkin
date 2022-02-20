from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.shortcuts import render
from django.urls import reverse, reverse_lazy

from authors.models import Post
from authors.forms import PostCreateViewForm

from myauth.models import MyUser

from django.views.generic import ListView, DetailView, CreateView


def index(request):
    return render(request, 'authors/index.html')


def list_post_by_author(request, name_id):
    posts = Post.objects.filter(name_id=name_id).select_related('name').all()
    context = {'posts': posts}
    return render(request, 'authors/post_list_author.html', context)


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
    paginate_by = 5

    def get_queryset(self):
        qs = MyUser.objects.filter(post__isnull=False)\
            .values('first_name', 'last_name', 'id')\
            .annotate(total=Count('id')).order_by('last_name')
        return qs


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostCreateViewForm

    def form_valid(self, form):
        form.instance.name_id = self.request.user.id
        return super().form_valid(form)

    def get_success_url(self):
        name_id = self.object.name_id
        return reverse_lazy('authors:list_post_by_author', kwargs={'name_id': name_id})

