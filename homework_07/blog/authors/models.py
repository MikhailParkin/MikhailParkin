from django.db import models

# Create your models here.


class Authors(models.Model):
    name = models.CharField(max_length=64, unique=True)
    email = models.EmailField(unique=True)
    rating = models.IntegerField()

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Имя автора'
        verbose_name_plural = 'Имена авторов'
        ordering = ['name']


class Post(models.Model):
    name = models.ForeignKey(Authors, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    body = models.TextField()

    def __str__(self):
        return f'Author: {self.name}  Title: {self.title}'

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ['name']


class Tag(models.Model):
    name = models.CharField(max_length=64)
    tag = models.ManyToManyField(Post)

    def __str__(self):
        return self.name
