from django.contrib import admin
from .models import MailingRecipient, Message, Mailing, SendingAttempt


@admin.register(MailingRecipient)
class MailingRecipientAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name', 'comment')
    search_fields = ('full_name',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'body',)
    search_fields = ('subject',)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('first_sent_at', 'ended_at', 'status', 'message', 'get_recipients',)
    list_filter = ('status',)
    search_fields = ('first_sent_at', 'ended_at',)

    def get_recipients(self, obj):
        return ", ".join([recipient.email for recipient in obj.recipients.all()])

    get_recipients.short_description = 'Получатели'


@admin.register(SendingAttempt)
class SendingAttemptAdmin(admin.ModelAdmin):
    list_display = ('mailing', 'attempt_time', 'status', 'response')
    list_filter = ('status',)
    search_fields = ('mailing__message__subject',)
