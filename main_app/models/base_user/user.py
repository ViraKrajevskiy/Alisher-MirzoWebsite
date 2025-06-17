from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

# базовая модель которая считывает время когда обновлен и создан
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

# создание кастомногго моделя пользователя
class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, email=None, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('Поле ввода номера телефона не должно быть пустым!')
        user = self.model(phone_number=phone_number, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_admin(self, phone_number, email=None, password=None, **extra_fields):
        extra_fields.setdefault('role', 'admin')
        extra_fields.setdefault('is_admin', True)
        if not phone_number:
            raise ValueError('Поле ввода номера телефона не должно быть пустым!')
        return self.create_user(phone_number, email, password, **extra_fields)


    def create_guest(self, phone_number, email=None, password=None, **extra_fields):
        extra_fields.setdefault('role', 'guest')
        extra_fields.setdefault('is_guest', True)
        if not phone_number:
            raise ValueError('Поле ввода номера телефона не должно быть пустым!')
        return self.create_user(phone_number, email, password, **extra_fields)

    def create_superuser(self, phone_number, email=None, password=None, **extra_fields):
        extra_fields.setdefault('role', 'supervisor')
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        return self.create_user(phone_number, email, password, **extra_fields)


# и сам базовый класс вместо базового класса джанго
class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    class Role(models.TextChoices):
        ADMIN = 'admin', 'Админ'
        GUEST = 'guest', 'Гость'
        SUPERVISOR = 'supervisor', 'Глава'

    phone_regex = RegexValidator(
        regex=r'^\+998\d{9}$',
        message="Номер телефона должен быть в формате +998XXXXXXXX!"
    )

    username = models.CharField(max_length=150, unique=True, null=True, blank=True)

    email = models.EmailField(unique=True, null=True, blank=True)
    phone_number = models.CharField(validators=[phone_regex], max_length=13, unique=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.GUEST)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone_number'  # для логина используем всё ещё телефон
    REQUIRED_FIELDS = ['email', 'username']  # username обязателен при создании через createsuperuser

    def __str__(self):
        return f"{self.get_role_display()} - {self.phone_number} - {self.username or ''}"

    def is_role(self, role):
        return self.role == role
