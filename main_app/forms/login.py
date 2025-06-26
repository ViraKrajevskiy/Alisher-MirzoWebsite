

from django import forms
from django.contrib.auth import authenticate
from main_app.models.base_user.user import User

class UsernameOrEmailLoginForm(forms.Form):
    username_or_email = forms.CharField(label="Email или Имя пользователя")
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")

    def clean(self):
        cleaned_data = super().clean()
        identifier = cleaned_data.get('username_or_email')
        password = cleaned_data.get('password')

        user = None
        if '@' in identifier:
            try:
                user_obj = User.objects.get(email=identifier)
                user = authenticate(username=user_obj.phone_number, password=password)
            except User.DoesNotExist:
                raise forms.ValidationError("Пользователь с таким email не найден.")
        else:
            try:
                user_obj = User.objects.get(username=identifier)
                user = authenticate(username=user_obj.phone_number, password=password)
            except User.DoesNotExist:
                raise forms.ValidationError("Пользователь с таким именем не найден.")

        if not user:
            raise forms.ValidationError("Неверный пароль.")

        cleaned_data['user'] = user
        return cleaned_data

    def get_user(self):
        return self.cleaned_data.get('user')
