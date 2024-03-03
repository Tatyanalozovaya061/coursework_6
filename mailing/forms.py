from django import forms
from django.forms import DateTimeInput

from mailing.models import Mail, Message, Client


class StyleFormMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class MailForm(StyleFormMixin, forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        user = self.request.user
        super().__init__(*args, **kwargs)
        self.fields['client'].queryset = Client.objects.filter(owner=user)
        self.fields['message'].queryset = Message.objects.filter(owner=user)

    class Meta:
        model = Mail
        exclude = ('next_date', 'owner', 'status', 'is_active',)

        widgets = {
            'start_date': DateTimeInput(
                attrs={'placeholder': 'ДД.ММ.ГГГГ ЧЧ:ММ:СС', 'type': 'datetime-local'}),
            'end_date': DateTimeInput(
                attrs={'placeholder': 'ДД.ММ.ГГГГ ЧЧ:ММ:СС', 'type': 'datetime-local'}),
        }

    def clean(self):
        data = self.cleaned_data
        if 'start_date' in data.keys() and 'end_date' in data.keys():
            start_date = data['start_date']
            end_date = data['end_date']
            if start_date >= end_date:
                raise forms.ValidationError('Дата окончания рассылки должна быть больше даты начала')


class MessageForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Message
        exclude = ('owner',)


class ClientForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Client
        exclude = ('owner',)
