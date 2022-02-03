from django.shortcuts import render
from django.urls import reverse_lazy

from django.views.generic import CreateView, DetailView, UpdateView, ListView

from myauth.forms import MyUserCreateForm, MyUserUpdateViewForm
from myauth.models import MyUser


class MyUserCreateView(CreateView):
    model = MyUser
    success_url = '/'
    form_class = MyUserCreateForm


class UserDetailView(DetailView):
    model = MyUser


class UserUpdateView(UpdateView):
    model = MyUser
    pk_url_kwarg = 'item_pk'
    form_class = MyUserUpdateViewForm

    def get_success_url(self):
        user_id = self.object.id
        return reverse_lazy('myauth:user_detail', kwargs={'pk': user_id})



