from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordResetForm, SetPasswordForm
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


# Nuevo: Formulario para solicitar restablecimiento
class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label='Correo electrónico',
        max_length=254,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingresa tu correo electrónico',
            'autocomplete': 'email'
        })
    )


# Nuevo: Formulario para establecer nueva contraseña
class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label='Nueva contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingresa tu nueva contraseña',
            'autocomplete': 'new-password'
        }),
        strip=False,
    )
    new_password2 = forms.CharField(
        label='Confirmar nueva contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirma tu nueva contraseña',
            'autocomplete': 'new-password'
        }),
        strip=False,
    )        