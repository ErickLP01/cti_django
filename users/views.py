from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LoginForm, RegisterForm
from .models import UserRole, Role, User
from django.http import HttpResponse

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':  
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = LoginForm()

    return render(request, 'users/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'You have successfully logged out.')
    return redirect('login')


def password_reset(request):
    return render(request, 'users/password_reset.html')


def home(request):
    return render(request, 'users/home.html')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Usuario registrado correctamente. Ahora puedes iniciar sesión.')
            return redirect('login')
        else:
            messages.error(request, 'Por favor corrige los errores del formulario.')
    else:
        form = RegisterForm()

    return render(request, 'users/register.html', {'form': form})


def create_superuser(request):
    User = get_user_model()
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin1234'
        )
        return HttpResponse("Superusuario creado exitosamente.")
    else:
        return HttpResponse("Ya existe un superusuario.")