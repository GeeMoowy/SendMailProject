from django.urls import path

from mailings.views import (RecipientsView, RecipientCreateView, HomePageView, RecipientDetailView, RecipientUpdateView,
                            RecipientDeleteViews, MessageListView, MessageCreateView, MessageDetailView, MessageUpdateView,
                            MessageDeleteViews)

app_name = 'recipients'

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('recipients/', RecipientsView.as_view(), name='recipients'),
    path('add_recipients/', RecipientCreateView.as_view(), name='add_recipients'),
    path('<int:pk>/recipient_detail/', RecipientDetailView.as_view(), name='recipient_detail'),
    path('<int:pk>/recipient_update/', RecipientUpdateView.as_view(), name='recipient_update'),
    path('<int:pk>/recipient_delete/', RecipientDeleteViews.as_view(), name='recipient_delete'),
    path('messages/', MessageListView.as_view(), name='messages'),
    path('add_message/', MessageCreateView.as_view(), name='add_message'),
    path('<int:pk>/message_detail/', MessageDetailView.as_view(), name='message_detail'),
    path('<int:pk>/message_update/', MessageUpdateView.as_view(), name='message_update'),
    path('<int:pk>/message_delete/', MessageDeleteViews.as_view(), name='message_delete'),
]