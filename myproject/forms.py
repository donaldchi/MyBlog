from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from myblog.models import MyBlog, Tag, MyReference
from myblog.models import MyEvent, ToDo
from django.contrib.auth import logout, authenticate, login
from django import forms
from django.template.defaultfilters import slugify
from markdownx.fields import MarkdownxFormField
from markdownx.widgets import MarkdownxWidget

#================ Blog Search ========================
class BlogSearchForm(forms.Form):
    search_blog =  forms.CharField( required = False, )

#================ Blog ========================
class BlogCreateForm(forms.ModelForm):
    tags = forms.CharField(required = True, help_text='Add tags by separating by comma(,).')
    # body = MarkdownxFormField();
    def save_data(self, user=None):
        instance = super(BlogCreateForm, self).save(commit=False)
        instance.slug = slugify(self.cleaned_data['title'])
        instance.slug = slugify(instance.title, required = True)
        instance.author = user
        instance.save()
        tags = self.cleaned_data['tags'].split(',')
        for item in tags:
            tag, status = Tag.objects.get_or_create(name=item.strip())
            self.instance.tags.add(tag)
        return instance

    class Meta:
        model = MyBlog
        fields = ['title', 'body', 'slug', 'genre', 'ref_title1', 'ref_url1', 'ref_title2', 'ref_url2', 
        'ref_title3', 'ref_url3', 'ref_title4', 'ref_url4', 
        'ref_title5', 'ref_url5']
        widgets = {
            'title': forms.TextInput(attrs = {'class': 'form-control'})
            #'body': MarkdownxWidget(attrs = {'class': 'form-control'})
        }

#================ MyBlog ========================
class BlogForm(forms.ModelForm):
    class Meta:
        model = MyBlog
        exclude = ['author', 'slug']

#================ Tag ========================
class TagCreateForm(forms.ModelForm):

    class Meta:
        model = Tag
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs = {'class': 'form-control'}), 
            'description': MarkdownxWidget(attrs = {'class': 'form-control'})
        }


#================ Event ========================
class EventCreateForm(forms.ModelForm):

    class Meta:
        model = MyEvent
        fields = ['name', 'description', 'url']
        widgets = {
            'name': forms.TextInput(attrs = {'class': 'form-control'}), 
            'description': MarkdownxWidget(attrs = {'class': 'form-control'})
        }


#================ Reference ========================
class ReferenceCreateForm(forms.ModelForm):

    class Meta:
        model = MyReference
        fields = ['name', 'description', 'url']
        widgets = {
            'name': forms.TextInput(attrs = {'class': 'form-control'}), 
            'description': MarkdownxWidget(attrs = {'class': 'form-control'})
        }

#================ User ========================
class RegisterForm(UserCreationForm):

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_staff = False
        if commit:
            user.save()
        return user
    class Meta:
        model = User
        fields = ("username", 'first_name', 'last_name', 'email', )


class LogoutForm(forms.Form):

    def logout(self, request):
        logout(request)
        return True

class LoginForm(forms.Form):
    print("LoginForm")

    username = forms.CharField(required=True, label="Username")
    password = forms.CharField(required=True, widget=forms.PasswordInput)
    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput, label="Remember Me?")

    def authenticate(self, request):
        data = self.cleaned_data
        user = authenticate(username=data["username"], password=data["password"])
        if user is not None:
            if user.is_active:
                if user.is_staff:
                    login(request, user)
                    if not data['remember_me']:
                        request.session.set_expiry(0)
                    return True
                else:
                    raise Exception("Your account is disabled!")
            else:
                raise Exception("Your account is disabled!")

        else:
            raise Exception("Your username and password were incorrect.")
        return False

#================ Todo ========================
class TodoCreateForm(forms.ModelForm):

    class Meta:
        model = ToDo
        fields = ['title', 'description', 'source_url', 'slug', 'status', 'progress', 
        'ref_title1', 'ref_url1', 'ref_title2', 'ref_url2', 
        'ref_title3', 'ref_url3', 'ref_title4', 'ref_url4', 
        'ref_title5', 'ref_url5']

        widgets = {
            'title': forms.TextInput(attrs = {'class': 'form-control'}), 
            'description': MarkdownxWidget(attrs = {'class': 'form-control'})
        }
