from django.urls import path

from mailings.views import RecipientsView, RecipientCreateView, HomePageView

app_name = 'recipients'

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('recipients/', RecipientsView.as_view(), name='recipients'),
    path('add_recipients/', RecipientCreateView.as_view(), name='add_recipients'),
]