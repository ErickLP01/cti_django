"""
WSGI config for cti project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cti.settings')

application = get_wsgi_application()

# Crea un superusuario automático si no existe
from django.contrib.auth import get_user_model
User = get_user_model()

if not User.objects.filter(username='administrador').exists():
    User.objects.create_superuser('administrador', 'admin@example.com', 'admin1234')
