from datetime import datetime, timedelta
import pytz
from django.core.mail import send_mail
from django.conf import settings
from mailing.models import Mail, Log


def my_job():
    day = timedelta(days=1, hours=0, minutes=0)
    week = timedelta(days=7, hours=0, minutes=0)
    month = timedelta(days=30, hours=0, minutes=0)

    mails = Mail.objects.all().filter(status='Создана') \
        .filter(is_active=True) \
        .filter(next_date__lte=datetime.now(pytz.timezone('Europe/Moscow'))) \
        .filter(end_date__gte=datetime.now(pytz.timezone('Europe/Moscow')))

    for mail in mails:
        mail.status = 'Запущена'
        mail.save()
        emails_list = [client.email for client in mail.mail_to.all()]

        result = send_mail(
            subject=mail.message.title,
            message=mail.message.content,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=emails_list,
            fail_silently=False,
        )

        if result == 1:
            status = 'Отправлено'
        else:
            status = 'Ошибка отправки'

        log = Log(mailing=mail, status=status)
        log.save()

        if mail.interval == 'once_a_day':
            mail.next_date = log.last_mailing_time + day
        elif mail.interval == 'once_a_week':
            mail.next_date = log.last_mailing_time + week
        elif mail.interval == 'once_a_month':
            mail.next_date = log.last_mailing_time + month

        if mail.next_date < mail.end_date:
            mail.status = 'Создана'
        else:
            mail.status = 'Завершена'
        mail.save()
