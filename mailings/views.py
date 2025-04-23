from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, TemplateView
from mailings.models import MailingRecipient


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


class RecipientDetailView(DeleteView):
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