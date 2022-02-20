from django.forms import ModelForm
from authors.models import Post


class PostCreateViewForm(ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'body',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field_obj in self.fields.items():
            field_obj.widget.attrs['class'] = 'form-control'
