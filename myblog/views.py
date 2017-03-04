from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from myblog.models import MyBlog
# from .forms import MyBlogForm

def index(request):
	if request.GET.get('all') == '1':
		queryset = MyBlog.objects.all()
	else:
		# queryset = MyBlog.objects.filter(done=False)
		queryset = MyBlog.objects.all()
		

	#作成日時順で降順にソート
	blog_list = queryset.order_by('-created_at')

	return render(request, ('blog_list.html'), {'blog_list' : blog_list})