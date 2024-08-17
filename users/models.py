from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from lms.models import Course, Lesson
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


class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Наличные'),
        ('transfer', 'Перевод на счет'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name='Пользователь'
    )
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата оплаты')
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='course_payments',
        verbose_name='Оплаченный курс'
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='lesson_payments',
        verbose_name='Отдельно оплаченный урок'
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма оплаты')
    payment_method = models.CharField(
        max_length=8,
        choices=PAYMENT_METHOD_CHOICES,
        default='transfer',
        verbose_name='Способ оплаты'
    )

    def __str__(self):
        return f"Оплата по {self.user} на {self.date}"

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
