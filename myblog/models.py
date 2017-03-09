from django.contrib.auth.models import User
from django.db import models
from markdownx.models import MarkdownxField


class Tag(models.Model):
    name = models.CharField(max_length=255)
    # description = models.CharField(max_length=255, null=True, default='')
    description = MarkdownxField()

    def __str__(self):
        return self.name


class MyBlog(models.Model):
    title = models.CharField(max_length=255)
    # body = models.CharField(max_length=20000)
    # body = models.TextField()
    body = MarkdownxField()

    tags = models.ManyToManyField(Tag)
    author = models.ForeignKey(User, null=True)
    publishing_date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField()

    def __str__(self):
        return self.title