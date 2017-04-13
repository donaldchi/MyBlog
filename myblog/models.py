from django.contrib.auth.models import User
from django.db import models
from markdownx.models import MarkdownxField
from myblog.choices import *;
from django.utils.encoding import python_2_unicode_compatible
from updown.fields import RatingField
from ckeditor.fields import RichTextField

@python_2_unicode_compatible
class Tag(models.Model):
    name = models.CharField(max_length=255)
    description = MarkdownxField()

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class MyBlog(models.Model):
    title = models.CharField(max_length=255)
    # body = MarkdownxField()
    body = RichTextField(verbose_name="default")


    tags = models.ManyToManyField(Tag)
    author = models.ForeignKey(User, null=True)
    publishing_date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField()

    rating = RatingField(can_change_vote=True)

    genre = models.IntegerField(choices=GENRE_CHOICES, default=0)
    
    ref_title1 = models.CharField(max_length=255, default=' ', blank=True)
    ref_url1 = models.URLField(blank=True, null=True)

    ref_title2 = models.CharField(max_length=255, default=' ', blank=True)
    ref_url2 = models.URLField(blank=True, null=True)

    ref_title3 = models.CharField(max_length=255, default=' ', blank=True)
    ref_url3 = models.URLField(blank=True, null=True)

    ref_title4 = models.CharField(max_length=255, default=' ', blank=True)
    ref_url4 = models.URLField(blank=True, null=True)

    ref_title5 = models.CharField(max_length=255, default=' ', blank=True)
    ref_url5 = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title

@python_2_unicode_compatible
class MyService(models.Model):
    name = models.CharField(max_length=255)
    description = MarkdownxField()
    url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name   
    
# class MyComment(models.Model):
#     author = models.CharField(max_length=255)
#     body = MarkdownxField()
#     publishing_date = models.DateTimeField(auto_now_add=True)
#     post = models.ForeignKey(MyBlog)
#     def __str__(self):
#         return self.body
@python_2_unicode_compatible
class MyReference(models.Model):
    name = models.CharField(max_length=255)
    description = MarkdownxField()
    publishing_date = models.DateTimeField(auto_now_add=True)
    url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class MyEvent(models.Model):
    name = models.CharField(max_length=255)
    description = MarkdownxField()
    publishing_date = models.DateTimeField(auto_now_add=True)
    url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class ToDo(models.Model):
    title = models.CharField(max_length=1000)
    description = MarkdownxField()
    slug = models.SlugField( default='')

    publishing_date = models.DateTimeField(auto_now_add=True)
    source_url = models.URLField(blank=True, null=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    progress = models.IntegerField(choices=PROGRESS_CHOICES, default=0)
    
    ref_title1 = models.CharField(max_length=255, default=' ', blank=True)
    ref_url1 = models.URLField(blank=True, null=True)

    ref_title2 = models.CharField(max_length=255, default=' ', blank=True)
    ref_url2 = models.URLField(blank=True, null=True)

    ref_title3 = models.CharField(max_length=255, default=' ', blank=True)
    ref_url3 = models.URLField(blank=True, null=True)

    ref_title4 = models.CharField(max_length=255, default=' ', blank=True)
    ref_url4 = models.URLField(blank=True, null=True)

    ref_title5 = models.CharField(max_length=255, default=' ', blank=True)
    ref_url5 = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title
