from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, TemplateView, DetailView
from mailings.models import MailingRecipient, Message


class HomePageView(TemplateView):
    template_name = 'mailings/home.html'


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
        return reverse('recipients:recipient_detail', args=[self.kwargs.get('pk')])


class MessageDeleteViews(DeleteView):
    model = Message
    template_name = 'mailings/message_confirm_delete.html'
    success_url = reverse_lazy('recipients:messages')
    context_object_name = 'message'
