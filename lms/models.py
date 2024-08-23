from django.db import models
from utils.const import NULLABLE
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.urls import reverse


class Course(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название курса")
    preview = models.ImageField(
        upload_to="courses/", **NULLABLE, verbose_name="Превью (картинка)"
    )
    description = models.TextField(verbose_name="Описание курса")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        **NULLABLE,
        related_name='courses',
        verbose_name="Владелец курса"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, **NULLABLE, verbose_name='Цена')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
    time_last_send = models.DateTimeField(default=timezone.now, verbose_name='Время последнего уведомления')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def get_absolute_url(self):
        return reverse('lms:course-detail', kwargs={'pk': self.pk})


class Lesson(models.Model):
    course = models.ForeignKey(Course, related_name="lessons", on_delete=models.CASCADE)
    title = models.CharField(
        max_length=255,
        verbose_name="Название урока",
        help_text="Укажите название урока",
    )
    description = models.TextField(
        verbose_name="Описание урока", help_text="Укажите описание урока"
    )
    preview = models.ImageField(
        upload_to="lessons/",
        **NULLABLE,
        verbose_name="Превью (картинка)",
        help_text="Укажите превью урока"
    )
    video_url = models.URLField(**NULLABLE, verbose_name="Ссылка на видео", help_text="Укажите ссылку на видео урока")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        **NULLABLE,
        related_name='lessons',
        verbose_name="Владелец урока"
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def get_absolute_url(self):
        return reverse('lms:lesson-detail', kwargs={'pk': self.pk})


class Subscription(models.Model):
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='subscription',
        **NULLABLE,
        verbose_name='Владелец'
    )
    course = models.ForeignKey(
        to=Course,
        on_delete=models.CASCADE,
        related_name='subscription',
        **NULLABLE,
        verbose_name='Курс'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ['id']

    def __str__(self):
        user = self.user or 'Неизвестный'
        course = self.course or 'Удалено'
        return f'{user} подписался на {course}'
