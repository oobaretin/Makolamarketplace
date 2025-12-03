"""
Forms for orders app.
"""
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from .models import Order


class CheckoutForm(forms.ModelForm):
    """Form for checkout process."""
    class Meta:
        model = Order
        fields = ['shipping_address', 'phone', 'email', 'notes']
        widgets = {
            'shipping_address': forms.Textarea(attrs={
                'class': 'form-textarea',
                'rows': 4,
                'placeholder': 'Enter your full shipping address'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Phone number'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': 'Email address'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-textarea',
                'rows': 3,
                'placeholder': 'Special delivery instructions (optional)'
            }),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Pre-fill form if user is authenticated
        if user and user.is_authenticated:
            self.fields['email'].initial = user.email
            self.fields['phone'].initial = user.phone
            self.fields['shipping_address'].initial = user.get_full_address()
        
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'email',
            'phone',
            'shipping_address',
            'notes',
            Submit('submit', 'Proceed to Payment', css_class='btn btn-primary w-full')
        )

