from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Book
from django import forms

class ExampleForm(forms.Form):
    title = forms.CharField(max_length=100, label='Book Title')

class BookSearchForm(forms.Form):
    title = forms.CharField(max_length=100)

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
