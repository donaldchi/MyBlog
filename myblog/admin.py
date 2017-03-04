from django.contrib import admin

# Register your models here.

from django import forms

from .models import MyBlog, Tag

admin.site.register(MyBlog)
admin.site.register(Tag)