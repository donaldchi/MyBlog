#-*- coding: utf-8 -*-
from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse
from myblog.models import *

class BlogSitemap(Sitemap):
    
    protocol = "https"
    priority = 1.0

    def items(self):
        return MyBlog.objects.all()
    
    def lastmod(self, obj):
        return obj.publishing_date

    def location(self, obj):
        return "/details/" + str(obj.slug) + "/"

    def changefreq(self, obj):
        return "daily"

class ToDoSitemap(Sitemap):
    
    protocol = "https"
    priority = 0.8

    def items(self):
        return ToDo.objects.all()
    
    def lastmod(self, obj):
        return obj.publishing_date

    def location(self, obj):
        return "/todo/details/" + str(obj.slug) + "/"

    def changefreq(self, obj):
        return "always"

class StaticViewSitemap(Sitemap):
    
    protocol = "https"
    priority = 0.5

    def items(self):
        return ['policy', 'inquiry', 'feed']

    def location(self, item):
        return reverse(item)

    def changefreq(self, obj):
        return "daily"