from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from main_app.models.base_user.user import User

class PhoneNumberForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['phone_number']

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number']

class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label="Старый пароль", widget=forms.PasswordInput)
    new_password1 = forms.CharField(label="Новый пароль", widget=forms.PasswordInput)
    new_password2 = forms.CharField(label="Подтвердите новый пароль", widget=forms.PasswordInput)
