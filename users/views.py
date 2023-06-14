

# Create your views here.
from django.shortcuts import render
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
# importar raise_exception




from django.views.generic import (
    View,
    CreateView
)

from django.views.generic.edit import (
    FormView
)

from .forms import (
    UserRegisterForm, 
    LoginForm,
    UpdatePasswordForm,
    VerificationForm,ForgotPasswordForm
)
#
from .models import User
# 
from .functions import code_generator


class UserRegisterView(FormView):
    template_name = 'users/Vlogin.html'
    form_class = UserRegisterForm
    success_url = '/'

    def form_valid(self, form):
        # generamos el codigo
        codigo = code_generator()
        #
        usuario = User.objects.create_user(
            form.cleaned_data['username'],
            form.cleaned_data['email'],
            form.cleaned_data['password1'],
            name=form.cleaned_data['name'],
            lastname =form.cleaned_data['lastname'],
            telephone=form.cleaned_data['telephone'],
            codregistro=codigo
        )
        # enviar el codigo al email del user
        asunto = 'Confrimacion de email'
        mensaje = 'Codigo de verificacion: ' + codigo
        email_remitente = 'informacion@codensolar.com'
        usuario_new=[form.cleaned_data['email']]
        print(usuario_new)

        
        email=EmailMessage(asunto, 
                           mensaje, 
                           email_remitente, 
                           [form.cleaned_data['email']])
        email.send()        
        #
        #send_mail(asunto, mensaje, email_remitente, [form.cleaned_data['email'],])
        # redirigir a pantalla de valdiacion

        return HttpResponseRedirect(
            reverse(
                'users_app:user-verification',
                kwargs={'pk': usuario.id}
            )
        )



class LoginUser(FormView):
    template_name = 'users/login1.html'
    form_class = LoginForm
    success_url = 'http://54.173.145.183/products/shopping_car/0'

    def form_valid(self, form):
        user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password']
        )
        print(user, '------------------')
        login(self.request, user)
        return super(LoginUser, self).form_valid(form)


class LogoutView(View):

    def get(self, request, *args, **kargs):
        logout(request)
        return HttpResponseRedirect(
            reverse(
                'users_app:user-login'
            )
        )
    
class ForgotpasswordView(FormView):
    template_name = 'users/update.html'
    form_class = ForgotPasswordForm
    success_url = reverse_lazy('users_app:user-login')

    def form_valid(self, form):
        codigo = code_generator()
        # detectar si enviaron el username o el email
        email = form.cleaned_data['email']
        user=User.objects.get(email=email)
        
        asunto = 'Recuperar contraseña'
        mensaje = 'Contraseña provisional: ' + codigo
        email_remitente = 'informacion@codensolar.com'
        #
        if user:
            email=EmailMessage(asunto, mensaje, email_remitente, [form.cleaned_data['email'],])
            user.set_password(codigo)
            user.save()
            
        else:
            # levantar error usuario no existe
            form.add_error('email', 'El email no existe')
            return HttpResponseRedirect(
                reverse(
                    'users_app:user-forgotpassword'
                )
            
            )
        return super(ForgotpasswordView, self).form_valid(form)

        


class UpdatePasswordView(LoginRequiredMixin, FormView):
    template_name = 'users/update.html'
    form_class = UpdatePasswordForm
    success_url = reverse_lazy('users_app:user-login')
    login_url = reverse_lazy('users_app:user-login')

    def form_valid(self, form):
        usuario = self.request.user
        user = authenticate(
            username=usuario.username,
            password=form.cleaned_data['password1']
        )

        if user:
            new_password = form.cleaned_data['password2']
            usuario.set_password(new_password)
            usuario.save()

        logout(self.request)
        return super(UpdatePasswordView, self).form_valid(form)


class CodeVerificationView(FormView):
    template_name = 'users/activate.html'
    form_class = VerificationForm
    success_url = '/login'

    def get_form_kwargs(self):
        kwargs = super(CodeVerificationView, self).get_form_kwargs()
        kwargs.update({
            'pk': self.kwargs['pk'],
        })
        return kwargs

    def form_valid(self, form):
        #
        User.objects.filter(
            id=self.kwargs['pk']
        ).update(
            is_active=True
        )
        
        return super(CodeVerificationView, self).form_valid(form)