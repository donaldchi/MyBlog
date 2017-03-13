import json
import collections
from pytz import timezone
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.shortcuts import render_to_response, get_object_or_404
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

#========== Todo =================
class TodoListView(ListView):
    model = ToDo
    template_name = "todo_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
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
        context = super().get_context_data(**kwargs)
        return context

#========== About Blog =================
class BlogListView(ListView):
    model = MyBlog
    template_name = "blog_list.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        #add tag to model
        context.update({
            'tags': Tag.objects.all(),
            'projects': ToDo.objects.all().order_by('-publishing_date'),
            'refs': MyReference.objects.all().order_by('-publishing_date'),
            'events': MyEvent.objects.all().order_by('-publishing_date'),
        })

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
        return context

    def get_queryset(self):
        return MyBlog.objects.order_by('publishing_date')

class BlogDetailView(DetailView):
    model = MyBlog
    template_name = 'blog_details.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        #add tag to model
        context.update({
            'blog_list': MyBlog.objects.order_by('-publishing_date'),
        })
        return context
# class BlogDetailView(request, slug):
#     post = get_object_or_404(MyBlog, slug=slug)
#     form = CommentForm(request.POST or None)
#     def view_post(request, slug):
#     if form.is_valid():
#         comment = form.save(commit=False)
#         comment.post = post
#         comment.save()
#         request.session["author"] = comment.author
#         request.session["body"] = comment.body
#         return redirect(request.path)

#     form.initial['author'] = request.session.get('author')
#     form.initial['body'] = request.session.get('body')
#     return render_to_response('blog_post.html',
#         {
#           'post': post,
#           'form': form,
#           'blog_list': MyBlog.objects.order_by('-publishing_date'),
#         },
#         context_instance=RequestContext(request))


class BlogCreateView(CreateView):
    model = MyBlog
    form_class = BlogCreateForm
    template_name = 'blog_create.html'
    success_url = '/'
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save_data(user=request.user)
            return super().form_valid(form)
        else:
            return super().form_invalid(form)

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

class TagCreateView(CreateView):
    model = Tag
    form_class = TagCreateForm
    template_name = 'create.html'
    success_url = '/tags/'

class TagListView(SingleTableView):
    model = Tag
    template_name = 'tag_list.html'
    table_class = TagTable

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
        context = super().get_context_data(**kwargs)
        
        event_list = MyEvent.objects.all().order_by('-publishing_date')

        #set page
        page = int(self.request.GET.get('page')) -1 if self.request.GET.get('page') else None
        if page and page>0:
            context['object_list'] = event_list[page*6-1: page*6+6]
        else: 
            context['object_list'] = event_list[0:6]
        pagination = list()
        for i in range(int(event_list.count()/6)+1):
            pagination.append(i+1)
        context['pagination'] = pagination
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
        context = super().get_context_data(**kwargs)
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
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.authenticate(request)
            return super().post(request, *args, **kwargs)
        else:
            return redirect("/login")

class LogoutView(FormView):
    form_class = LogoutForm
    success_url = "/"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        form.logout(request)
        return super().form_valid(form)

#========== RSS Feed =================
from django.http import JsonResponse
#coding : utf-8
class JsonResponseView(ListView):
    model = MyBlog
    template_name = 'tag_list.html'

    def get(self, request, *args, **kwargs):
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