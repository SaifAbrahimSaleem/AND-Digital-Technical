from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django import forms
from .models import User

class ContactForm(forms.Form):
    contact_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name', 'name':'contact_name'}), label='Name')
    contact_email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email', 'name':'contact_email'}), label='Contact Email')
    contact_number = forms.CharField(required=True, max_length=11, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number', 'name':'contact_number'}), label='Phone Number')
    contact_content = forms.CharField(required=True, widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Message', 'name':'contact_content'}), label='Message')

class LoginForm(forms.Form):
    email = forms.EmailField(required=True, max_length=60, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email', 'id':'login_email', 'name':'email', 'type':'email'}), label='Email')
    password = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'type':'password','placeholder': 'Password', 'name':'password'}), label='Password')
    class Meta:
        model = User
        fields = ('email', 'password')

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        email = self.cleaned_data.get('email')
        print(email)
        password = self.cleaned_data.get('password')
        print(password)
        print(authenticate(email=email, password=password))
        if not authenticate(email=email, password=password):
            raise forms.ValidationError("Invalid Login Credentials")

class RegisterForm(UserCreationForm):
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username', 'id':'register_username', 'name':'username'}), label='Username')
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name', 'id':'register_first', 'name':'first_name'}), label='Name')
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name', 'id':'register_last', 'name':'last_name'}), label='Last Name')
    email = forms.EmailField(required=True, max_length=60, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email', 'id':'register_email', 'name':'email'}), label='Email')
    password1  = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'password','id':'register_password', 'placeholder': 'Password', 'name':'password1'}), label='Password')
    password2  = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'password','id':'register_confirm_password', 'placeholder': 'Confirm Password', 'name':'password2'}), label='Confirm Password')

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password1', 'password2')