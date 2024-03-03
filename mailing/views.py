import random

from django.contrib.auth.decorators import login_required, permission_required
from django.http import Http404
from django.shortcuts import redirect

from blog.models import Blog
from mailing.forms import ClientForm, MailForm, MessageForm
from mailing.models import Client, Mail, Message, Log
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class MailListView(LoginRequiredMixin, ListView):
    model = Mail


class MailCreateView(LoginRequiredMixin, CreateView):
    model = Mail
    form_class = MailForm
    success_url = reverse_lazy('mailing:mail_list')
    extra_context = {
        'title': 'Создание рассылки'
    }

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class MailDetailView(LoginRequiredMixin, DetailView):
    model = Mail

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if (self.object.owner != self.request.user and not self.request.user.is_superuser
                and not self.request.user.is_staff):
            raise Http404
        return self.object


class MailUpdateView(LoginRequiredMixin, UpdateView):
    model = Mail
    form_class = MailForm
    success_url = reverse_lazy('mailing:mail_list')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_superuser:
            raise Http404
        return self.object

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs


class MailDeleteView(LoginRequiredMixin, DeleteView):
    model = Mail
    success_url = reverse_lazy('mailing:mail_list')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_superuser:
            raise Http404
        return self.object


class HomeView(ListView):
    model = Mail
    template_name = 'mailing/home.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['mail_count'] = len(Mail.objects.all())
        context_data['active_mail_count'] = len(Mail.objects.filter(is_active=True))
        context_data['clients_count'] = len(Client.objects.all())
        blogs = list(Blog.objects.all())
        random.shuffle(blogs)
        context_data['blogs'] = blogs[:3]
        return context_data


class ClientListView(LoginRequiredMixin, ListView):
    model = Client

    def get(self, request):
        if self.request.user.is_staff and not self.request.user.is_superuser:
            raise Http404
        return super().get(request)


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    # permission_required = 'client.add_client'
    success_url = reverse_lazy('mailing:client_list')

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_superuser:
            raise Http404
        return self.object


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    fields = ('fullname', 'email', 'comment')

    def get_success_url(self):
        return reverse('mailing:client_view', args=[self.object.pk])

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_superuser:
            raise Http404
        return self.object


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('mailing:client_list')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_superuser:
            raise Http404
        return self.object


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailing:message_list')
    extra_context = {
        'title': 'Создание сообщения'
    }

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    extra_context = {
        'title': 'Список сообщений'
    }

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = Message.objects.filter(owner=self.request.user)
        return queryset


class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm

    def get_success_url(self):
        return reverse('mailing:message_view', args=[self.kwargs.get('pk')])


class MessageDetailView(DetailView):
    model = Message


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('mailing:message_list')


class LogListView(LoginRequiredMixin, ListView):
    model = Log

    def get(self, request):
        if self.request.user.is_staff and not self.request.user.is_superuser:
            raise Http404
        return super().get(request)


class LogDeleteView(LoginRequiredMixin, DeleteView):
    model = Log
    success_url = reverse_lazy('mailing:log_list')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_superuser:
            raise Http404
        return self.object
