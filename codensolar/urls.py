"""codensolar URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

from users.models import User
from django.contrib.auth import get_user_model

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def is_auto_signup_allowed(self, request, sociallogin):
        print('is_auto_signup_allowed')
        print("El correo electrónico del usuario social ya existe", sociallogin.user.email)
        # Si el correo electrónico del usuario social ya existe, no permitir el auto signup.
        if User.objects.filter(email=sociallogin.user.email).exists():
            print("El correo electrónico del usuario social ya existe", sociallogin.user.email)
            return False
        return super().is_auto_signup_allowed(request, sociallogin)
    
    def is_email_verified(self, provider, email):
        print('is_email_verified')
        # Si no viene el correo, imprimir en consola "No hay correo"
        if not email:
            print("No hay correo")
        else:
            # Buscar entre los usuarios y activar el usuario si se encuentra el correo
            user_model = get_user_model()
            try:
                user = user_model.objects.get(email=email)
                user.is_active = True
                user.save()
            except user_model.DoesNotExist:
                print("No se encontró el correo en la base de datos de usuarios")
        return super().is_email_verified(provider, email)
    
    def populate_user(self, request, sociallogin, data):
        print('populate_user/************-*/')
        print(data)

        return super().populate_user(request, sociallogin, data)

    
    

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')), # home app
    path('user/', include('users.urls')),
    path('products/', include('products.urls')),
    path('accounts/', include('allauth.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)