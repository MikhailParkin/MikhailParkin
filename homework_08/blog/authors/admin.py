from django.contrib import admin

from authors.models import Authors, Post, Tag
# Register your models here.

admin.site.register(Authors)
admin.site.register(Post)
admin.site.register(Tag)


