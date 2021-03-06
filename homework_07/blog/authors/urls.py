from django.urls import path

import authors.views as authors


app_name = 'authors'

urlpatterns = [
    path('', authors.index, name='index'),
    path('posts/', authors.PostsListView.as_view(), name='posts_list'),
    path('authors/', authors.AuthorsListView.as_view(), name='authors_list'),
    path('authors/<int:pk>/', authors.PostDetailView.as_view(), name='post_detail'),

]
