import re

from django import forms
from django.core.exceptions import ValidationError

from .models import ContactRequest

UA_PHONE_RE = re.compile(
    r'^\+?3?8?\s*\(?\s*0\d{2}\s*\)?\s*\d{3}[\s\-]?\d{2}[\s\-]?\d{2}$'
)


def validate_ua_phone(value):
    digits = re.sub(r'\D', '', value)
    if not UA_PHONE_RE.match(value) or len(digits) not in (10, 12):
        raise ValidationError(
            'Введіть коректний номер телефону, наприклад: +38 (067) 123-45-67'
        )


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactRequest
        fields = ['name', 'phone', 'object_type']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': "Ваше ім'я",
                'class': 'form-input',
            }),
            'phone': forms.TextInput(attrs={
                'placeholder': '+38 (0__) ___-__-__',
                'class': 'form-input',
                'type': 'tel',
                'inputmode': 'tel',
            }),
            'object_type': forms.TextInput(attrs={
                'placeholder': "Тип об'єкта (необов'язково)",
                'class': 'form-input',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['object_type'].required = False
        self.fields['phone'].validators.append(validate_ua_phone)
