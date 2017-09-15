#! /usr/bin/env python  
# -*- coding: UTF-8 -*-  
import json
import collections
from pytz import timezone
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
#from django.shortcuts import render_to_response, get_object_or_404
#from django.http import Http404
from django.utils.safestring import mark_safe
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, FormView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import generic
from django_tables2 import SingleTableView
import django_tables2 as tables
from django_tables2.utils import A

# Create your views here.
from myblog.models import MyBlog, Tag, ToDo, MyEvent, MyReference
from myproject.forms import BlogCreateForm, TodoCreateForm, BlogSearchForm
from myproject.forms import RegisterForm, LoginForm, LogoutForm
from myproject.forms import TagCreateForm, EventCreateForm, ReferenceCreateForm

# For Search List View
from search_views.search import SearchListView
from search_views.filters import BaseFilter

from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response

GENRES = {
    "life" : 1,
    "coding" : 2,
    "recruit" : 3,
    "project" : 4,
    "ai" : 5,
    "others" : 6
}

#========== Counter =================
def getTime():#get current time
    import time
    return time.ctime()

def getCount(slug):#get visit time        
    import os.path
    count = 0
    countfile = None
    print(os.path.dirname(os.path.abspath(__file__)))
    if os.path.isfile('/Library/WebServer/Documents/myproject/count/'+slug.encode('utf-8')+".dat") :
        countfile = open('/Library/WebServer/Documents/myproject/count/'+slug.encode('utf-8')+".dat", 'r+')
        counttext = countfile.read()   
        count = int(counttext)+1
    else:
        countfile = open('/Library/WebServer/Documents/myproject/count/'+slug.encode('utf-8')+".dat", 'w')
        count = 1 
    countfile.seek(0)
    countfile.truncate()#clear file
    countfile.write(str(count))#write counter
    countfile.flush()
    countfile.close()   
    return count

#========== Policy =================
def policy(request):
    return render(request, 'policy.html', {})

#========== Inquiry Form =================
def inquiry(request):
    return render(request, 'mail.html', {})

#========== Todo =================
class TodoListView(ListView):
    model = ToDo
    template_name = "todo_list.html"

    def get_context_data(self, **kwargs):
        context = super(TodoListView, self).get_context_data(**kwargs)
        
        project_list = ToDo.objects.all().order_by('-publishing_date')

        #set page
        page = int(self.request.GET.get('page')) -1 if self.request.GET.get('page') else None
        if page and page>0:
            context['project_list'] = project_list[page*6-1: page*6+6]
        else: 
            context['project_list'] = project_list[0:6]
        pagination = list()
        for i in range(int(project_list.count()/6)+1):
            pagination.append(i+1)
        context['pagination'] = pagination
        return context

    def get_queryset(self):
        return ToDo.objects.order_by('publishing_date')


class TodoCreateView(CreateView):
    model = ToDo
    form_class = TodoCreateForm
    template_name = 'create.html'
    success_url = '/'

class TodoDetailView(DetailView):
    model = ToDo
    template_name = 'todo_details.html'

    def get_context_data(self, **kwargs):
        context = super(TodoDetailView, self).get_context_data(**kwargs)

        count = getCount(context['object'].slug)
        context.update({
            'count' : count,
        })

        return context

#========== About Blog =================
class BlogListView(ListView):
    model = MyBlog
    template_name = "blog_list.html"

    def get_context_data(self, **kwargs):
        genre = self.request.GET.get('genre')
        tag = self.request.GET.get('tag_param')

        context = super(BlogListView, self).get_context_data(**kwargs)
        
        count = getCount('blog_list_page')
        #add tag to model
        context.update({
            'tags': Tag.objects.all(),
            'projects': ToDo.objects.all().order_by('-publishing_date'),
            'refs': MyReference.objects.all().order_by('-publishing_date'),
            'events': MyEvent.objects.all().order_by('-publishing_date'),
            'count' : count,
        })

        blog_list = None
        if genre:
            blog_list = MyBlog.objects.filter(genre=GENRES[genre]).order_by('-publishing_date')
        elif tag:
            blog_list = MyBlog.objects.filter(tags__name=tag).order_by('-publishing_date')
        else:
            blog_list = MyBlog.objects.all().order_by('-publishing_date')

        #set page
        page = int(self.request.GET.get('page')) -1 if self.request.GET.get('page') else None
        if page and page>0:
            context['object_list'] = blog_list[page*6-1: page*6+6]
        else: 
            context['object_list'] = blog_list[0:6]
        pagination = list()
        for i in range(int(blog_list.count()/6)+1):
            pagination.append(i+1)
        context['pagination'] = pagination
        context['genre'] = genre
        #set tag cloud

        tags = Tag.objects.all()
        tag_weight = dict()
        records = list()
        blog_list = None        
        for tag in tags:
            tag_weight_dict = dict()
            blog_list = MyBlog.objects.filter(tags__name=tag).order_by('-publishing_date')
            print("tag name: ", tag.name, " count: ", blog_list.count())
            
            tag_weight_dict["text"] = tag.name
            tag_weight_dict["weight"] = blog_list.count()

            records.append(tag_weight_dict)
        
        context['tag_weight'] = records

        return context

    def get_queryset(self):
        return MyBlog.objects.order_by('publishing_date')

class BlogDetailView(DetailView):
    model = MyBlog
    template_name = 'blog_details.html'


    def get_context_data(self, **kwargs):
        context = super(BlogDetailView, self).get_context_data(**kwargs)
        
        time = getTime()
        count = getCount(context['object'].slug)

        #add tag to model
        context.update({
            'blog_list': MyBlog.objects.order_by('-publishing_date'),
            'count' : count,
            'time' : time,
        })

        return context

class BlogCreateView(CreateView):
    model = MyBlog
    form_class = BlogCreateForm
    template_name = 'blog_create.html'
    success_url = '/'
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save_data(user=request.user)
            return super(BlogCreateView, self).form_valid(form)
        else:
            return super(BlogCreateView, self).form_invalid(form)

class BlogFilter(BaseFilter):
    search_fields = {
        'search_blog' : ['title', 'body'],
    }

class BlogSearchList(SearchListView):
    model = MyBlog
    # paginate_by = 100
    template_name = "search_result.html"
    form_class = BlogSearchForm
    filter_class = BlogFilter

#=================Tag =================
class TagTable(tables.Table):
    select = tables.CheckBoxColumn(accessor='pk')
    name = tables.LinkColumn('tag_details', args=[A('pk')])

    def render_description(self, **kwargs):
        return mark_safe(kwargs['value'])
    class Meta:
        model= Tag
        sequence = 'select', 'name', 'description'
        exclude = {'id'}
        attrs = {"class": "paleblue"}

class TagListView(ListView):
    model = Tag
    template_name = "tag_list.html"

    def get_context_data(self, **kwargs):
        context = super(TagListView, self).get_context_data(**kwargs)
        #set tag cloud
        tags = Tag.objects.all()
        tag_weight = dict()
        records = list()
        blog_list = None        
        for tag in tags:
            tag_weight_dict = dict()
            blog_list = MyBlog.objects.filter(tags__name=tag).order_by('-publishing_date')
            print("tag name: ", tag.name, " count: ", blog_list.count())
            
            tag_weight_dict["text"] = tag.name
            tag_weight_dict["weight"] = blog_list.count()

            records.append(tag_weight_dict)
        
        context['tag_weight'] = records

        return context

    def get_queryset(self):
        return Tag.objects.all()


class TagCreateView(CreateView):
    model = Tag
    form_class = TagCreateForm
    template_name = 'create.html'
    success_url = '/tags/'

class TagDetailView(DetailView):
    model = Tag
    template_name = 'tag_details.html'

#================= Event =================
class EventCreateView(CreateView):
    model = MyEvent
    form_class = EventCreateForm
    template_name = 'create.html'
    success_url = '/event/'

class EventListView(ListView):
    model = MyEvent
    template_name = 'event_list.html'
    def get_context_data(self, **kwargs):
        context = super(EventListView, self).get_context_data(**kwargs)
        
        event_list = MyEvent.objects.all().order_by('-publishing_date')

        count = getCount('event_list_page')
        context.update({
            'count' : count,
        })

        return context

    def get_queryset(self):
        return MyEvent.objects.order_by('publishing_date')

class EventDetailView(DetailView):
    model = MyEvent
    template_name = 'event_details.html'

#========== Reference =================

class ReferenceCreateView(CreateView):
    model = MyReference
    form_class = ReferenceCreateForm
    template_name = 'create.html'
    success_url = '/reference/'

class ReferenceListView(ListView):
    model = MyReference
    template_name = 'reference_list.html'
    def get_context_data(self, **kwargs):
        context = super(ReferenceListView, self).get_context_data(**kwargs)
        ref_list = MyReference.objects.all().order_by('-publishing_date')
        #set page
        page = int(self.request.GET.get('page')) -1 if self.request.GET.get('page') else None
        if page and page>0:
            context['object_list'] = ref_list[page*6-1: page*6+6]
        else: 
            context['object_list'] = ref_list[0:6]
        pagination = list()
        for i in range(int(ref_list.count()/6)+1):
            pagination.append(i+1)
        context['pagination'] = pagination
        return context

    def get_queryset(self):
        return MyReference.objects.order_by('publishing_date')

class ReferenceDetailView(DetailView):
    model = MyReference
    template_name = 'reference_details.html'


#========== About User =================
class RegisterUserView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = "create.html"
    success_url = "/"

class LoginView(FormView):
    template_name = "create.html"
    form_class = LoginForm
    success_url = "/"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect("/")
        return super(LoginView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.authenticate(request)
            return super(LoginView, self).post(request, *args, **kwargs)
        else:
            return redirect("/login")

class LogoutView(FormView):
    form_class = LogoutForm
    success_url = "/"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        form.logout(request)
        return super(LogoutView, self).form_valid(form)

#========== RSS Feed =================
from django.http import JsonResponse
#coding : utf-8
from django.http import JsonResponse
#coding : utf-8
class JsonResponseView(ListView):
    model = MyBlog
    template_name = 'tag_list.html'

    def get(self, request, *args, **kwargs):
        slug_param = self.request.GET.get('slug')
        print("slug from url: ", slug_param)
        if slug_param is None :
            response_content = collections.OrderedDict()
            response_content["length"] = len(MyBlog.objects.all())
            count = 0
            for item in MyBlog.objects.all():
                data = collections.OrderedDict()
                data['title'] = item.title
                jst_now = item.publishing_date.astimezone(timezone('Asia/Tokyo'))
                data['date'] =  jst_now.strftime("%Y-%m-%d %H:%M:%S")
                data['author'] = str(item.author)
                data['body'] = item.body
                data['slug'] = item.slug
                data['tags'] = ', '.join([x.name for x in item.tags.all()])
                response_content["item"+str(count)] = data
                count = count+1
            json_str = json.dumps(response_content, ensure_ascii=False, indent=2)
            response = HttpResponse(json_str, content_type='application/json; charset=UTF-8')
            return response
        else:
            response_content = collections.OrderedDict()
            print("slug_param: ", slug_param)
            blog_object = MyBlog.objects.filter(slug=slug_param)
            response_content["length"] = len(blog_object)
            item = blog_object[0];
            response_content['title'] = item.title
            jst_now = item.publishing_date.astimezone(timezone('Asia/Tokyo'))
            response_content['date'] =  jst_now.strftime("%Y-%m-%d %H:%M:%S")
            response_content['author'] = str(item.author)
            response_content['body'] = item.body
            response_content['slug'] = item.slug
            response_content['tags'] = ', '.join([x.name for x in item.tags.all()])

            json_str = json.dumps(response_content, ensure_ascii=False, indent=2)
            response = HttpResponse(json_str, content_type='application/json; charset=UTF-8')
            return response


#=============== api =============
import smtplib
from email.MIMEText import MIMEText
from email.Utils import formatdate

def create_message(name, subject, body):
    msg = MIMEText(body, _subtype='plain')
    msg['Subject'] = subject
    msg['From'] = name + '<donald-2@163.com>'
    msg['To'] = 'donald-2@163.com'
    return msg

def send(msg):
    try:
        mail_host="smtp.163.com"
        mail_user="donald-2"
        mail_pass="tiancai05370219"
        me = 'donald-2@163.com'
        
        s = smtplib.SMTP()
        s.connect(mail_host)
        s.login(mail_user, mail_pass)
        s.sendmail(me, me, msg.as_string())
        s.close()
        return True
    except Exception, e:
        print str(e)
        return False

def check_mail_param(param):
    if "name" not in param.keys():
        return False, "Please input your name"
    if "from_addr" not in param.keys():
        return False, "Please input email address"
    if "title" not in param.keys():
        return False, "Please input title"
    if "msg" not in param.keys():
        return False, "Please input msg"
    return True, "success"

@api_view(['POST'])
@permission_classes(())
def send_mail_api(request, format=None):
    if request.method == 'POST':
        result = {'result': '0', "msg" : "error"}
        param = request.data
        is_valid, msg = check_mail_param(param)
        if is_valid:
            from_addr = param["from_addr"]
            name = param["name"]
            title = param["title"]
            msg = param["msg"]

            from_addr = from_addr.encode('utf-8')
            name = name.encode('utf-8')
            title = "お問い合わせ from ganbaruyo.net: " + title.encode('utf-8')
            msg = msg.encode('utf-8')

            msg = "Name:  " + name + "\n\nEmail:  " + from_addr + "\n\nMessage:  " + msg


            mail_msg = create_message(name, title, msg)
            if send(mail_msg):
                result = {
                    "result" : 1,
                    "msg" :  "Message has been sent successfully.",
                }
            else:
                result = {
                    "result" : 0,
                    "msg" :  "Error when sending.",
                }             
        else:
            result = {
                "result" : 0,
                "msg": msg,
            }
        return Response(result, status=status.HTTP_200_OK)
    return Response({"result" : 0, "msg":"No method implemented for " + request.method}, status=status.HTTP_400_BAD_REQUEST)
