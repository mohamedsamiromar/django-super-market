from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    brith_day = forms.DateField(help_text='Required, format: YYYY-MM-DD')

    class Meta:
        model = User
        fields = ('username', 'brith_day', 'password1', 'password2')
