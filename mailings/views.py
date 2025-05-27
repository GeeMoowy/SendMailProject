from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, TemplateView, DetailView
from mailings.models import MailingRecipient, Message, Mailing, SendingAttempt
from django.contrib import messages
from django.shortcuts import redirect


class HomePageView(TemplateView):
    template_name = 'mailings/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        total_mailings = Mailing.objects.count()
        active_mailings = Mailing.objects.filter(status='started').count()
        unique_recipients = MailingRecipient.objects.values('email').distinct().count()

        context['total_mailings'] = total_mailings
        context['active_mailings'] = active_mailings
        context['unique_recipients'] = unique_recipients
        context['user'] = self.request.user

        return context


class RecipientsView(LoginRequiredMixin, ListView):
    model = MailingRecipient
    template_name = 'mailings/recipients.html'
    context_object_name = 'recipients'

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.request.user.has_perm('mailings.can_view_all_recipients'):
            return queryset
        return queryset.filter(owner=self.request.user)


class RecipientCreateView(LoginRequiredMixin, CreateView):
    model = MailingRecipient
    fields = ('email', 'full_name', 'comment')
    template_name = 'mailings/add_recipients.html'
    success_url = reverse_lazy('recipients:recipients')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class RecipientDetailView(DetailView):
    model = MailingRecipient
    template_name = 'mailings/recipient_detail.html'
    context_object_name = 'recipient'


class RecipientUpdateView(UpdateView):
    model = MailingRecipient
    fields = ('email', 'full_name', 'comment')
    template_name = 'mailings/add_recipients.html'
    success_url = reverse_lazy('recipients:recipients')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        # Разрешаем если: пользователь владелец ИЛИ менеджер/админ (но только просмотр)
        if obj.owner != request.user and not request.user.is_superuser:
            raise PermissionDenied("Вы не можете редактировать чужие данные")
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('recipients:recipient_detail', args=[self.kwargs.get('pk')])


class RecipientDeleteViews(DeleteView):
    model = MailingRecipient
    template_name = 'mailings/recipient_confirm_delete.html'
    success_url = reverse_lazy('recipients:recipients')
    context_object_name = 'recipient'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        # Только владелец может удалять (даже менеджеры не могут удалять чужие данные)
        if obj.owner != request.user:
            raise PermissionDenied("Вы не можете удалять чужие данные")
        return super().dispatch(request, *args, **kwargs)


class MessageListView(ListView):
    model = Message
    template_name = 'mailings/messages.html'
    context_object_name = 'messages'

    def get_queryset(self):
        return Message.objects.all()


class MessageCreateView(CreateView):
    model = Message
    fields = ('subject', 'body')
    template_name = 'mailings/add_message.html'
    success_url = reverse_lazy('recipients:messages')


class MessageDetailView(DetailView):
    model = Message
    template_name = 'mailings/message_detail.html'
    context_object_name = 'message'


class MessageUpdateView(UpdateView):
    model = Message
    fields = ('subject', 'body')
    template_name = 'mailings/add_message.html'
    success_url = reverse_lazy('recipients:messages')

    def get_success_url(self):
        return reverse('recipients:message_detail', args=[self.kwargs.get('pk')])


class MessageDeleteViews(DeleteView):
    model = Message
    template_name = 'mailings/message_confirm_delete.html'
    success_url = reverse_lazy('recipients:messages')
    context_object_name = 'message'


class MailingListView(ListView):
    model = Mailing
    template_name = 'mailings/mailing.html'
    context_object_name = 'mailing'

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.request.user.has_perm('mailings.can_view_all_mailing'):
            return queryset
        return queryset.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_manager'] = self.request.user.groups.filter(name='Менеджеры').exists()
        return context


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    fields = ('first_sent_at', 'ended_at', 'status', 'message', 'recipients')
    template_name = 'mailings/add_mailing.html'
    success_url = reverse_lazy('recipients:mailing')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MailingDetailView(DetailView):
    model = Mailing
    template_name = 'mailings/mailing_detail.html'
    context_object_name = 'mailing'


class MailingUpdateView(UpdateView):
    model = Mailing
    fields = ('first_sent_at', 'ended_at', 'status', 'message', 'recipients')
    template_name = 'mailings/add_mailing.html'
    success_url = reverse_lazy('recipients:mailing')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        # Разрешаем если: пользователь владелец ИЛИ менеджер/админ (но только просмотр)
        if obj.owner != request.user and not request.user.is_superuser:
            raise PermissionDenied("Вы не можете редактировать чужие данные")
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('recipients:mailing_detail', args=[self.kwargs.get('pk')])


class MailingDeleteViews(DeleteView):
    model = Mailing
    template_name = 'mailings/mailing_confirm_delete.html'
    success_url = reverse_lazy('recipients:mailing')
    context_object_name = 'mailing'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        # Только владелец может удалять (даже менеджеры не могут удалять чужие данные)
        if obj.owner != request.user:
            raise PermissionDenied("Вы не можете удалять чужие данные")
        return super().dispatch(request, *args, **kwargs)


class SendMailingView(View):
    def post(self, request, pk):
        mailing = Mailing.objects.get(pk=pk)
        recipients = mailing.recipients.all()

        for recipient in recipients:
            attempt = SendingAttempt(mailing=mailing)  # Создаем новую попытку для каждого получателя
            try:
                send_mail(
                    subject=mailing.message.subject,
                    message=mailing.message.body,
                    from_email='kovylek.ul@mail.ru',
                    recipient_list=[recipient.email],
                    fail_silently=False,
                )

                attempt.status = 'Успешно'
                attempt.response = 'Письмо успешно отправлено.'
                messages.success(request, f'Письмо успешно отправлено на {recipient.email}.')

            except Exception as e:
                attempt.status = 'Не успешно'
                attempt.response = str(e)
                messages.error(request, f'Ошибка при отправке письма на {recipient.email}: {str(e)}')

            attempt.save()  # Сохраняем попытку после обработки

        messages.success(request, 'Рассылка завершена!')
        return redirect('mailings:mailing_attempts', pk=mailing.pk)


class AllSendingAttemptsView(View):
    def get(self, request):
        attempts = SendingAttempt.objects.all()
        return render(request, 'mailings/all_attempts.html', {'attempts': attempts})


class MailingAttemptsView(ListView):
    model = SendingAttempt
    template_name = 'mailings/mailing_attempts.html'
    context_object_name = 'attempts'

    def get_queryset(self):
        mailing_id = self.kwargs['pk']
        return SendingAttempt.objects.filter(mailing_id=mailing_id)


class MailingReportsView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    template_name = 'mailings/mailing_reports.html'
    permission_required = 'mailings.view_reports'
    context_object_name = 'user_reports'

    def get_queryset(self):
        # Базовый запрос
        queryset = Mailing.objects.all()

        # Для обычных пользователей - только свои рассылки
        if not self.request.user.has_perm('mailings.can_view_all'):
            queryset = queryset.filter(owner=self.request.user)

        # Собираем статистику по каждому пользователю
        reports = []
        for mailing in queryset:
            attempts = mailing.sending_attempts.all()
            total_attempts = attempts.count()
            success_attempts = attempts.filter(status='Успешно').count()
            failed_attempts = total_attempts - success_attempts

            reports.append({
                'mailing': mailing,
                'total_attempts': total_attempts,
                'success_attempts': success_attempts,
                'failed_attempts': failed_attempts,
                'success_rate': (success_attempts / total_attempts * 100) if total_attempts > 0 else 0,
                'last_attempt': attempts.order_by('-attempt_time').first()
            })

        return reports


class MailingAttemptsDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Mailing
    template_name = 'mailings/mailing_attempts_detail.html'
    permission_required = 'mailings.view_reports'
    context_object_name = 'mailing'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mailing = self.get_object()

        attempts = mailing.sending_attempts.all().order_by('-attempt_time')
        total = attempts.count()
        success = attempts.filter(status='Успешно').count()

        context.update({
            'attempts': attempts,
            'total_attempts': total,
            'success_attempts': success,
            'failed_attempts': total - success,
            'success_rate': (success / total * 100) if total > 0 else 0
        })
        return context


class DisableMailingView(PermissionRequiredMixin, View):
    def test_func(self):
        user = self.request.user
        return user.groups.filter(name='Менеджеры').exists() or user.has_perm('mailings.can_disable_mailing')

    def post(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk)
        mailing.status = 'disabled'
        mailing.save()

        messages.success(request, f'Рассылка "{mailing.message.subject}" отключена')
        return redirect('mailings:mailing')