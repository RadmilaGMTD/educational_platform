from django.conf import settings
from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название курса")
    image = models.ImageField(upload_to="materials/image", null=True, blank=True, verbose_name="Изображение курса")
    description = models.TextField(null=True, blank=True, verbose_name="Описание курса")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name="Владелец", null=True, blank=True
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return f"{self.name}"


class Lesson(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название урока")
    image = models.ImageField(upload_to="materials/image", null=True, blank=True, verbose_name="Изображение урока")
    description = models.TextField(null=True, blank=True, verbose_name="Описание урока")
    course = models.ForeignKey(
        Course, on_delete=models.SET_NULL, verbose_name="Курс", null=True, blank=True, related_name="lessons"
    )
    video_url = models.URLField(null=True, blank=True, verbose_name="Ссылка на видео")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name="Владелец", null=True, blank=True
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def __str__(self):
        return f"{self.name}"
