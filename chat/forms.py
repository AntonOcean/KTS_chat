from django.contrib.auth import password_validation
from django.contrib.auth.forms import AuthenticationForm, UsernameField, UserCreationForm
from django import forms

from chat.models import User


class ChatUserCreationForm(UserCreationForm):
    username = UsernameField(
        label = 'Имя пользователя',
        max_length=254,
        widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}),
    )
    password1 = forms.CharField(
        label=("Пароль"),
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label = ("Подтвердите пароль"),
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        strip=False,
        help_text =("Enter the same password as before, for verification."),
    )

    class Meta:
        model = User
        fields = ("username", "avatar")


class ChatLoginForm(AuthenticationForm):
    username = UsernameField(
        label = 'Имя пользователя',
        max_length=254,
        widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}),
    )
    password = forms.CharField(
        label='Пароль',
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
)