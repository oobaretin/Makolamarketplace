"""
Forms for accounts app.
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from .models import User


class UserRegistrationForm(UserCreationForm):
    """Custom user registration form."""
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-input'})
    )
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-input'})
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-input'})
    )
    phone = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-input'})
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'phone', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('first_name', css_class='form-group w-full md:w-1/2 px-3 mb-4'),
                Column('last_name', css_class='form-group w-full md:w-1/2 px-3 mb-4'),
            ),
            'username',
            'email',
            'phone',
            Row(
                Column('password1', css_class='form-group w-full md:w-1/2 px-3 mb-4'),
                Column('password2', css_class='form-group w-full md:w-1/2 px-3 mb-4'),
            ),
            Submit('submit', 'Register', css_class='btn btn-primary')
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class UserProfileForm(forms.ModelForm):
    """Form for updating user profile."""
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone', 'address', 'city', 'state', 'zip_code')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
            'phone': forms.TextInput(attrs={'class': 'form-input'}),
            'address': forms.TextInput(attrs={'class': 'form-input'}),
            'city': forms.TextInput(attrs={'class': 'form-input'}),
            'state': forms.TextInput(attrs={'class': 'form-input'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('first_name', css_class='form-group w-full md:w-1/2 px-3 mb-4'),
                Column('last_name', css_class='form-group w-full md:w-1/2 px-3 mb-4'),
            ),
            'phone',
            'address',
            Row(
                Column('city', css_class='form-group w-full md:w-1/2 px-3 mb-4'),
                Column('state', css_class='form-group w-full md:w-1/2 px-3 mb-4'),
            ),
            'zip_code',
            Submit('submit', 'Update Profile', css_class='btn btn-primary')
        )


class CustomAuthenticationForm(AuthenticationForm):
    """Custom authentication form with styling."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-input'})
        self.fields['password'].widget.attrs.update({'class': 'form-input'})

