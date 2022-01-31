from django.shortcuts import render
from authors.models import Post
# Create your views here.


def index(request):
    return render(request, 'authors/index.html')


def list_posts(request):
    posts = Post.objects.all()
    context = {'posts': posts}
    return render(request, 'authors/list_posts.html', context=context)
