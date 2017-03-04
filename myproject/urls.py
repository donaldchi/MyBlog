"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
#----------------Generic Views------------------
from django.views.generic import ListView
from django.views.generic import DetailView
#----------------Customized Views------------------
from myblog.views import BlogListView, BlogDetailView
from myblog.views import RegisterUserView, LogoutView, LoginView
#----------------Models------------------
from myblog.models import MyBlog, Tag

#----------------Authenticate------------------
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', BlogListView.as_view(), name='blog_list'),
    url(r'^details/(?P<slug>[-_\w]+)/$', BlogDetailView.as_view(), name='blog_details'),
    url(r'^register/$', RegisterUserView.as_view(), name='register_user'),
    url(r'^logout/$', login_required(LogoutView.as_view()), name='logout_user'),
    url(r'^login/$', LoginView.as_view(), name='login_user'),
]