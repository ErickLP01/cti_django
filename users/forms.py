from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import User
from captcha.fields import CaptchaField

class LoginForm(AuthenticationForm):
  
  captcha = CaptchaField()
  
  username = forms.CharField(
    label= 'Username',
    widget= forms.TextInput(attrs={
      'class': 'form-control',
      'placeholder': 'Enter your username'
    })
  )
  
  password = forms.CharField(
    label= 'Password',
    widget= forms.PasswordInput(attrs={
      'class': 'form-control',
      'placeholder': 'Enter your password'
    })
  )
  
  class Meta:
    model = User
    fields = ['username', 'password', 'captcha']