from django.db import models
from utils.const import NULLABLE


class Course(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название курса")
    preview = models.ImageField(
        upload_to="courses/", **NULLABLE, verbose_name="Превью (картинка)"
    )
    description = models.TextField(verbose_name="Описание курса")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


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
    video_url = models.URLField(
        verbose_name="Ссылка на видео", help_text="Укажите ссылку на видео урока"
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
