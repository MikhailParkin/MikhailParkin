from django.urls import path

from django.contrib.auth.views import LoginView, LogoutView
import myauth.views as myauth

app_name = 'myauth'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),

    path('user/create/', myauth.MyUserCreateView.as_view(),
         name='user_create'),

    path('logout/', LogoutView.as_view(),
         name='logout'),

    path('user/<int:pk>/', myauth.UserDetailView.as_view(),
         name='user_detail'),

    path('user/edit/<int:item_pk>/', myauth.UserUpdateView.as_view(),
         name='user_update'),

]
