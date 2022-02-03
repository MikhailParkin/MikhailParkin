from django.db import models
from myauth.models import MyUser

# Create your models here.


# class Authors(models.Model):
#     name = models.CharField(max_length=64)
#     email = models.EmailField()
#     rating = models.IntegerField(default=0)
#
#     def __str__(self):
#         return f'{self.name}'
#
#     class Meta:
#         verbose_name = 'Имя автора'
#         verbose_name_plural = 'Имена авторов'
#         ordering = ['name']


class Post(models.Model):
    name = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    body = models.TextField()

    def __str__(self):
        return f'{self.name}  Title: {self.title}'

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ['name']


class Tag(models.Model):
    name = models.CharField(max_length=64)
    tag = models.ManyToManyField(Post)

    def __str__(self):
        return self.name
