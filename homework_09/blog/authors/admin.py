from django.contrib import admin

from authors.models import Post, Tag
# Register your models here.

admin.site.register(Post)
admin.site.register(Tag)


