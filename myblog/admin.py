from django.contrib import admin
from django.db import models
from markdownx.admin import MarkdownxModelAdmin

from django import forms
from .models import MyBlog, Tag

# Register your models here.

class BlogForm(forms.ModelForm):
    body= forms.CharField(widget=forms.Textarea)
    class Meta:
        model = MyBlog
        fields = '__all__'


class BlogAdmin(admin.ModelAdmin):
    form = BlogForm
    filter_horizontal = ('tags',)
    
admin.site.register(MyBlog, MarkdownxModelAdmin)
# admin.site.register(MyBlog)
admin.site.register(Tag)
