from django import forms
from .models import Application


class ApplicationForm(forms.ModelForm):
    """Форма заявки"""
    
    class Meta:
        model = Application
        fields = ['company_name', 'contact_person', 'email', 'phone', 'message']
        widgets = {
            'company_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ваше имя или название компании'
            }),
            'contact_person': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Контактное лицо'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'email@example.com'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+7 (___) ___-__-__'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Опишите, какая услуга вам нужна',
                'rows': 4
            }),
        }
        labels = {
            'company_name': 'Ваше имя / Компания *',
            'contact_person': 'Контактное лицо',
            'email': 'Email',
            'phone': 'Телефон *',
            'message': 'Сообщение / Услуга',
        }
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '')
        # Удаляем все нецифровые символы
        digits = ''.join(filter(str.isdigit, phone))
        if len(digits) < 10:
            raise forms.ValidationError('Введите корректный номер телефона')
        return phone