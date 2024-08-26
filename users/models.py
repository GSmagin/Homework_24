from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils import timezone
from lms.models import Course, Lesson
from utils.const import NULLABLE

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Поле email должно быть установлено')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser должен иметь is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser должен иметь is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

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

    objects = UserManager()

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
    session_id = models.CharField(max_length=255, verbose_name="ID сессии в Stripe", **NULLABLE)
    link = models.URLField(max_length=400, verbose_name="Ссылка на оплату", **NULLABLE)

    def __str__(self):
        return f"Платеж от {self.user} на сумму {self.amount} от {self.date}"

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
