import secrets

from django.contrib.auth import logout
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import FormView, View, DetailView, UpdateView
from django.urls import reverse_lazy, reverse

from config.settings import EMAIL_HOST_USER
from users.forms import UserRegistrationForm, UserProfileForm
from users.models import CustomUser




class RegisterView(FormView):
    model = CustomUser
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/users/email-confirm/{token}/'
        send_mail(
            subject='Подтверждение почты',
            message=f'Привет, перейди по ссылке для подтверждения почты {url}',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})


class LogoutView(View):
    def post(self, request):
        logout(request)
        return redirect('users:login')

    def get(self, request):
        return self.post(request)


class ProfileDetailView(DetailView):
    model = CustomUser
    template_name = 'users/profile_detail.html'
    context_object_name = 'user'

    def get_object(self, queryset=None):
        return self.request.user


class ProfileEditView(UpdateView):
    model = CustomUser
    form_class = UserProfileForm
    template_name = 'users/profile_edit.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


def email_verification(request, token):
    user = get_object_or_404(CustomUser, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse('users:login'))
