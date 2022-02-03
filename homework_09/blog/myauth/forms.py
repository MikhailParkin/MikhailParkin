from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from myauth.models import MyUser


class MyUserCreateForm(UserCreationForm):
    class Meta:
        model = MyUser
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field_obj in self.fields.items():
            field_obj.help_text = ''
            field_obj.widget.attrs['class'] = 'form-control'
            # print(field_name, field_obj.help_text)


class MyUserUpdateViewForm(ModelForm):
    class Meta:
        model = MyUser
        fields = ('first_name', 'last_name', 'email', 'd_birth', 'bio',)
        labels = {'d_birth': 'Date birth'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field_obj in self.fields.items():
            field_obj.widget.attrs['class'] = 'form-control'
            print(field_name, field_obj.widget)

