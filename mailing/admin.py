from django.contrib import admin

from mailing.models import Client, Message, Mail, Log


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('email', 'fullname', 'comment',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject',)


@admin.register(Mail)
class MailAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'periodicity', 'status',)
    list_filter = ('start_date',)


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ('time_last_mailing', 'status',)
