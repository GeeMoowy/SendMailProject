from django.urls import path

from mailings.views import RecipientsView

app_name = 'recipients'

urlpatterns = [
    path('', RecipientsView.as_view(), name='recipients'),
]