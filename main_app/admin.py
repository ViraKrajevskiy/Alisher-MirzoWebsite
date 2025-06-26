from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from main_app.models.base_user.user import User
from main_app.models.model_book.book import ComentBook, Book
from main_app.models.model_news.news import News,Comment
from main_app.models.model_picture.picture import Picture,CommentPicture


# Форма создания пользователя
class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'phone_number', 'role')

    def clean_password2(self):
        pw1 = self.cleaned_data.get("password1")
        pw2 = self.cleaned_data.get("password2")
        if pw1 and pw2 and pw1 != pw2:
            raise forms.ValidationError("Пароли не совпадают")
        return pw2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

# Форма редактирования пользователя
class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(label="Хэш пароля (не редактируется)")

    class Meta:
        model = User
        fields = ('username', 'email', 'phone_number', 'role', 'is_active', 'is_superuser')

# Настройка отображения User в админке
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('username', 'email', 'phone_number', 'role', 'is_active', 'is_superuser')
    list_filter = ('role', 'is_active', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'phone_number', 'password')}),
        ('Права', {'fields': ('role', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'phone_number', 'role', 'password1', 'password2'),
        }),
    )
    search_fields = ('email', 'phone_number', 'username')
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions')

# Регистрируем всё
admin.site.register(User, UserAdmin)
admin.site.register(Book)
admin.site.register(ComentBook)
admin.site.register(News)
admin.site.register(Comment)
admin.site.register(Picture)
admin.site.register(CommentPicture)
