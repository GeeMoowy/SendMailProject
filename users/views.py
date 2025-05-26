import secrets

from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from django.core.mail import send_mail
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import FormView, View, DetailView, UpdateView, ListView
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


class UserListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = CustomUser
    template_name = 'users/user_list.html'
    context_object_name = 'users'
    permission_required = 'users.can_block_user'

    # Убрали paginate_by - теперь все пользователи будут на одной странице

    def get_queryset(self):
        queryset = super().get_queryset().exclude(id=self.request.user.id)

        # Фильтрация по статусу (активные/заблокированные)
        status = self.request.GET.get('status')
        if status == 'active':
            queryset = queryset.filter(is_active=True)
        elif status == 'blocked':
            queryset = queryset.filter(is_active=False)

        # Поиск по email или имени
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(email__icontains=search) |
                Q(username__icontains=search)
            )

        return queryset.order_by('-date_joined')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()  # Получаем полный queryset
        context['total_users'] = queryset.count()
        context['active_users'] = queryset.filter(is_active=True).count()
        context['blocked_users'] = context['total_users'] - context['active_users']
        return context


class ToggleUserStatusView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'users.can_block_user'
    http_method_names = ['post']  # Явно разрешаем только POST

    def post(self, request, pk):
        user = get_object_or_404(CustomUser, pk=pk)

        if user == request.user:
            messages.error(request, "Вы не можете заблокировать себя!")
        else:
            user.is_active = not user.is_active
            user.save()
            action = "разблокирован" if user.is_active else "заблокирован"
            messages.success(request, f"Пользователь {user.email} {action}")

        return redirect(request.META.get('HTTP_REFERER', reverse('users:user_list')))

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm(self.permission_required):
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
