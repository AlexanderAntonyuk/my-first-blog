from django import forms
from .models import Post
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text', 'photo')


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class LoginForm(AuthenticationForm):

    class Meta:
        model = User
        fields = ('username', 'password')
