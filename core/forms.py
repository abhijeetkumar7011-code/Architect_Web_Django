from django import forms
from .models import ContactMessage


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your name', 'class': 'field-input'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Your email', 'class': 'field-input'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Phone (optional)', 'class': 'field-input'}),
            'subject': forms.TextInput(attrs={'placeholder': 'Subject', 'class': 'field-input'}),
            'message': forms.Textarea(attrs={'placeholder': 'Tell us about your project', 'class': 'field-input', 'rows': 5}),
        }
