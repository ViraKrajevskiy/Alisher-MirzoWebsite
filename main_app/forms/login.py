from django import forms
from django.contrib.auth import authenticate, get_user_model

User = get_user_model()

class UsernameOrEmailLoginForm(forms.Form):
    username_or_email = forms.CharField(label="Email или имя пользователя")
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        self.user = None

    def clean(self):
        username_or_email = self.cleaned_data.get('username_or_email')
        password = self.cleaned_data.get('password')

        if username_or_email and password:
            self.user = authenticate(self.request, username=username_or_email, password=password)
            if self.user is None:
                raise forms.ValidationError("Неверный логин или пароль.")
        return self.cleaned_data

    def get_user(self):
        return self.user
        