from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
import threading
from .forms import LoginForm, RegisterForm, CustomPasswordResetForm, CustomSetPasswordForm
from .models import UserRole, Role, User


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
                messages.error(request, 'Usuario o contraseña inválidos.')
        else:
            messages.error(request, 'Por favor corrige los errores del formulario.')
    else:
        form = LoginForm()

    return render(request, 'users/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'Has cerrado sesión exitosamente.')
    return redirect('login')


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


# Vista personalizada para password reset con threading
class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')
    subject = 'Restablece tu contraseña'
    
    def form_valid(self, form):
        """
        Sobrescribe form_valid para enviar email en segundo plano
        IMPORTANTE: NO llamar a super().form_valid(form) porque bloquea
        """
        # Mostrar mensaje inmediatamente
        messages.success(
            self.request,
            'Si el correo existe en nuestro sistema, recibirás un enlace para restablecer tu contraseña.'
        )
        
        # Preparar opciones para el envío
        opts = {
            'use_https': self.request.is_secure(),
            'token_generator': self.token_generator,
            'from_email': self.from_email,
            'email_template_name': self.email_template_name,
            'subject_template_name': self.subject_template_name,
            'request': self.request,
            'html_email_template_name': self.html_email_template_name,
            'extra_email_context': self.extra_email_context,
        }
        
        # Función para enviar en thread
        def send_reset_email():
            try:
                form.save(**opts)
                print("Email de restablecimiento enviado correctamente")
            except Exception as e:
                print(f"Error enviando email: {str(e)}")
        
        # Iniciar thread y NO esperar a que termine
        email_thread = threading.Thread(target=send_reset_email)
        email_thread.daemon = True  # El thread se cerrará si la app se cierra
        email_thread.start()
        
        # Redirigir inmediatamente sin esperar al email
        return HttpResponseRedirect(self.get_success_url())


def password_reset_done_view(request):
    return render(request, 'users/password_reset_done.html')


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomSetPasswordForm
    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')
    
    def form_valid(self, form):
        messages.success(self.request, 'Tu contraseña ha sido cambiada exitosamente.')
        return super().form_valid(form)


def password_reset_complete_view(request):
    return render(request, 'users/password_reset_complete.html')