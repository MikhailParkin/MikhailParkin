from django.db import models

from django.contrib.auth.models import User, AbstractUser


class MyUser(AbstractUser):
    email = models.EmailField('email address', unique=True)
    d_birth = models.DateField(blank=True, null=True)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
