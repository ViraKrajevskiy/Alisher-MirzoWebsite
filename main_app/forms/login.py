from django import forms
from django.contrib.auth import authenticate, get_user_model
import re

User = get_user_model()

class UsernameOrEmailLoginForm(forms.Form):
    username_or_email = forms.CharField(label="Email или Имя пользователя")
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def clean_username_or_email(self):
        identifier = self.cleaned_data.get('username_or_email')
        if not identifier:
            raise forms.ValidationError("Это поле обязательно.")
        return identifier.strip()

    def clean(self):
        cleaned_data = super().clean()
        identifier = cleaned_data.get('username_or_email', '').strip()
        password = cleaned_data.get('password')

        if not identifier or not password:
            return cleaned_data

        is_email = re.match(r"[^@]+@[^@]+\.[^@]+", identifier)
        if is_email:
            print("[DEBUG] Это email")
            try:
                user_obj = User.objects.get(email__iexact=identifier)
                username = user_obj.get_username()
                print(f"[DEBUG] Найден username: {username}")
            except User.DoesNotExist:
                print("[DEBUG] Пользователь с таким email не найден.")
                raise forms.ValidationError("Пользователь с таким email не найден.")
        else:
            print("[DEBUG] Это username")
            username = identifier

        print(f"[DEBUG] Аутентификация: {username} / {password}")
        user = authenticate(request=self.request, username=username, password=password)

        print(f"[DEBUG] Результат authenticate: {user}")
        if not user:
            raise forms.ValidationError("Неверный email/имя пользователя или пароль.")
        if not user.is_active:
            raise forms.ValidationError("Этот аккаунт неактивен.")

        cleaned_data['user'] = user
        return cleaned_data

    def get_user(self):
        return self.cleaned_data.get('user')
