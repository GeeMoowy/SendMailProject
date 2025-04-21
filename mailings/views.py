from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from mailings.models import MailingRecipient


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
