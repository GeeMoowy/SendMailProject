from django.core.mail import send_mail
from django.shortcuts import render
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


class RecipientsView(ListView):
    model = MailingRecipient
    template_name = 'mailings/recipients.html'
    context_object_name = 'recipients'

    def get_queryset(self):
        return MailingRecipient.objects.all()


class RecipientCreateView(CreateView):
    model = MailingRecipient
    fields = ('email', 'full_name', 'comment')
    template_name = 'mailings/add_recipients.html'
    success_url = reverse_lazy('recipients:recipients')


class RecipientDetailView(DetailView):
    model = MailingRecipient
    template_name = 'mailings/recipient_detail.html'
    context_object_name = 'recipient'


class RecipientUpdateView(UpdateView):
    model = MailingRecipient
    fields = ('email', 'full_name', 'comment')
    template_name = 'mailings/add_recipients.html'
    success_url = reverse_lazy('recipients:recipients')

    def get_success_url(self):
        return reverse('recipients:recipient_detail', args=[self.kwargs.get('pk')])


class RecipientDeleteViews(DeleteView):
    model = MailingRecipient
    template_name = 'mailings/recipient_confirm_delete.html'
    success_url = reverse_lazy('recipients:recipients')
    context_object_name = 'recipient'


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
        return Mailing.objects.all()


class MailingCreateView(CreateView):
    model = Mailing
    fields = ('first_sent_at', 'ended_at', 'status', 'message', 'recipients')
    template_name = 'mailings/add_mailing.html'
    success_url = reverse_lazy('recipients:mailing')


class MailingDetailView(DetailView):
    model = Mailing
    template_name = 'mailings/mailing_detail.html'
    context_object_name = 'mailing'


class MailingUpdateView(UpdateView):
    model = Mailing
    fields = ('first_sent_at', 'ended_at', 'status', 'message', 'recipients')
    template_name = 'mailings/add_mailing.html'
    success_url = reverse_lazy('recipients:mailing')

    def get_success_url(self):
        return reverse('recipients:mailing_detail', args=[self.kwargs.get('pk')])


class MailingDeleteViews(DeleteView):
    model = Mailing
    template_name = 'mailings/mailing_confirm_delete.html'
    success_url = reverse_lazy('recipients:mailing')
    context_object_name = 'mailing'


class SendMailingView(View):
    def post(self, request, pk):
        mailing = Mailing.objects.get(pk=pk)
        recipients = mailing.recipients.all()
        attempt = SendingAttempt(mailing=mailing)
        attempt.save()

        for recipient in recipients:
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
                attempt.save()

            except Exception as e:

                attempt.status = 'Не успешно'
                attempt.response = str(e)
                attempt.save()
                messages.error(request, f'Ошибка при отправке письма на {recipient.email}: {str(e)}')
                break

        messages.success(request, 'Рассылка завершена!')
        return redirect('mailings:mailing_detail', pk=pk)
