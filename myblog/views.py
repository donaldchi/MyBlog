from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, FormView
from django.contrib.auth.models import User

# Create your views here.
from myblog.models import MyBlog
# from myproject.forms import BlogCreateForm
from myproject.forms import RegisterForm, LogoutForm, LoginForm


class BlogListView(ListView):
	model = MyBlog
	template_name = "blog_list.html"
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		blog_list = context['object_list']
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

class BlogDetailView(DetailView):
	model = MyBlog
	template_name = 'blog_details.html'

# class BlogCreateView(CreateView):
# 	model = MyBlog
# 	from_class = BlogCreateForm
# 	template_name = 'create.html'
# 	success_url = '/'

# 	def post(self, request, *args, **kwargs):
# 		form = self.form_class(request.POST)
# 		if form.is_valid():
# 			form.save_data(user=request.user)
# 			return super().form_valid(form)
# 		else:
# 			return super().form_invalid(form)

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