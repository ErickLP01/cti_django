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
    
    
class RegisterForm(UserCreationForm):
    captcha = CaptchaField()

    password1 = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingresa tu contraseña'
        })
    )

    password2 = forms.CharField(
        label='Confirmar contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirma tu contraseña'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'}),
        }