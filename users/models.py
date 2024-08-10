from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from utils.const import NULLABLE


class User(AbstractUser):
    username = None
    email = models.EmailField(
        max_length=50,
        unique=True,
        verbose_name="Электронная почта",
        help_text="Укажите электронную почту",
    )
    phone = models.CharField(
        max_length=15, **NULLABLE, verbose_name="Телефон", help_text="Укажите телефон"
    )
    city = models.CharField(
        max_length=100, **NULLABLE, verbose_name="Город", help_text="Укажите город"
    )
    avatar = models.ImageField(
        upload_to="users/avatars",
        **NULLABLE,
        verbose_name="Аватарка",
        help_text="Загрузите аватар"
    )
    date_joined = models.DateTimeField(default=timezone.now, verbose_name="Дата регистрации")
    last_login = models.DateTimeField(**NULLABLE, verbose_name="Дата последнего входа")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
