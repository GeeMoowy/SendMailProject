from django.contrib.auth import logout
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.views.generic import FormView, View
from django.urls import reverse_lazy

from users.forms import UserRegistrationForm
from users.models import CustomUser


class RegisterView(FormView):
    model = CustomUser
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        send_mail(
            'Добро пожаловать на мой сайт',
            'Вы зарегистрированы на сайте',
            'kovylek.ul@mail.ru',
            [user.email],
            fail_silently=False,
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
