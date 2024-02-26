from django.urls import path

from mailing.apps import MailingConfig
from mailing.views import ClientListView, ClientCreateView, ClientUpdateView, ClientDetailView, \
    ClientDeleteView, HomeView, MailListView, MailCreateView, MailDetailView, MailUpdateView, MailDeleteView, \
    MessageListView, MessageCreateView, MessageDetailView, MessageUpdateView, MessageDeleteView, LogListView, \
    LogDeleteView

app_name = MailingConfig.name


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('client/', ClientListView.as_view(), name='client_list'),
    path('client_create/', ClientCreateView.as_view(), name='client_create'),
    path('client_view/<int:pk>/', ClientDetailView.as_view(), name='client_view'),
    path('client_update/<int:pk>/', ClientUpdateView.as_view(), name='client_update'),
    path('client_delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),
    path('mail/', MailListView.as_view(), name='mail_list'),
    path('mail_create/', MailCreateView.as_view(), name='mail_create'),
    path('mail_view/<int:pk>', MailDetailView.as_view(), name='mail_view'),
    path('mail_update/<int:pk>/', MailUpdateView.as_view(), name='mail_update'),
    path('mail_delete/<int:pk>/', MailDeleteView.as_view(), name='mail_delete'),
    path('message/', MessageListView.as_view(), name='message_list'),
    path('message_create/', MessageCreateView.as_view(), name='message_create'),
    path('message_view/<int:pk>/', MessageDetailView.as_view(), name='message_view'),
    path('message_update/<int:pk>/', MessageUpdateView.as_view(), name='message_update'),
    path('message_delete/<int:pk>/', MessageDeleteView.as_view(), name='message_delete'),
    path('log', LogListView.as_view(), name='log_list'),
    path('log_delete/<int:pk>/', LogDeleteView.as_view(), name='log_delete')
]