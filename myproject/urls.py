from django.conf.urls import include, url

from django.contrib import admin
#----------------Generic Views------------------
from django.views.generic import ListView
from django.views.generic import DetailView
#----------------Customized Views------------------
from myblog.views import BlogListView, BlogDetailView, BlogCreateView
from myblog.views import RegisterUserView, LogoutView, LoginView
from myblog.views import TagListView, TagDetailView, TagCreateView
from myblog.views import JsonResponseView
from myblog.views import TodoListView, TodoCreateView, TodoDetailView
#----------------Models------------------
from myblog.models import MyBlog, Tag

#----------------Authenticate------------------
from django.contrib.auth.decorators import login_required

#----------------Set static to use javascript/css------------------
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', BlogListView.as_view(), name='blog_list'),
    url(r'^admin/', admin.site.urls),
    url(r'^details/(?P<slug>[-_\w]+)/$', BlogDetailView.as_view(), name='blog_details'),
    url(r'^blog/create/', login_required(BlogCreateView.as_view()), name='blog_create'),

    url(r'^tags/$', TagListView.as_view(), name='tag_list'),
    url(r'^tag/create/', login_required(TagCreateView.as_view()), name='tag_create'),
    url(r'^tags/details/(?P<pk>[0-9]+)/', TagDetailView.as_view(), name='tag_details'),

    url(r'^register/$', RegisterUserView.as_view(), name='register_user'),
    url(r'^logout/$', login_required(LogoutView.as_view()), name='logout_user'),
    url(r'^login/$', LoginView.as_view(), name='login_user'),

    url(r'^markdownx/', include('markdownx.urls')),

    url(r'^feed$', JsonResponseView.as_view(), name='feed'),

    url(r'^todo/$', TodoListView.as_view(), name='todo_list'),
    url(r'^todo/create/', TodoCreateView.as_view(), name='todo_create'),
    url(r'^todo/details/(?P<slug>[-_\w]+)/$', TodoDetailView.as_view(), name='todo_details'),

    
    url(r'^', include('django.contrib.staticfiles.urls')),
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)