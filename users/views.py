from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.core.exceptions import ImproperlyConfigured
from .forms import LoginForm, RegisterForm, CustomPasswordResetForm, CustomSetPasswordForm
from .models import UserRole, Role, User
from django.conf import settings
import logging


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
    subject_template_name = 'users/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')

    def form_valid(self, form):
        email = form.cleaned_data['email']

        # Validar que el email exista (opcional, por seguridad)
        if not User.objects.filter(email__iexact=email).exists():
            # logger.info(f"Intento de restablecimiento para email no registrado: {email}")
            messages.success(
                self.request,
                'Si el correo existe en nuestro sistema, recibirás un enlace para restablecer tu contraseña.'
            )
            return HttpResponseRedirect(self.get_success_url())

        try:
            # Enviar correo
            result = form.save(
                use_https=self.request.is_secure(),
                request=self.request,
                from_email=settings.DEFAULT_FROM_EMAIL,
            )
            # logger.info(f"Email de restablecimiento enviado a: {email}")
            messages.success(
                self.request,
                'Si el correo existe, recibirás un enlace para restablecer tu contraseña.'
            )
        except Exception as e:
            # logger.error(f"Error enviando email a {email}: {str(e)}")
            messages.error(self.request, 'Error temporal. Intenta de nuevo más tarde.')

        return HttpResponseRedirect(self.get_success_url())


# === CONFIRMACIÓN DE ENVÍO ===
def password_reset_done_view(request):
    return render(request, 'users/password_reset_done.html')


# === CONFIRMAR NUEVA CONTRASEÑA ===
class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomSetPasswordForm
    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')

    def form_valid(self, form):
        user = form.save()
        # logger.info(f"Contraseña restablecida para usuario: {user.username}")
        messages.success(self.request, '¡Tu contraseña ha sido cambiada exitosamente!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Las contraseñas no coinciden o son inválidas.')
        return super().form_invalid(form)


# === COMPLETADO ===
def password_reset_complete_view(request):
    return render(request, 'users/password_reset_complete.html')