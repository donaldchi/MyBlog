from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from myblog.models import MyBlog, Tag
from django.contrib.auth import logout, authenticate, login
from django import forms
from django.template.defaultfilters import slugify

class RegisterForm(UserCreationForm):

    def save(self, commit=True):
        user = super().save(commit=False)
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