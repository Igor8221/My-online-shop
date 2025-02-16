from django import forms
from apps.users.models import User
from .models import Order

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'address']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'required': 'required'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'required': 'required', 'rows': 3}),
        }
class OrderStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
