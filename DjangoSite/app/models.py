from pyexpat import model
from tabnanny import verbose
from django.db import models
from django.contrib import admin
from datetime import datetime
from django.urls import reverse
from django.contrib.auth.models import User


RATING_CHOICES = [
    (5, 'Отлично'),
    (4, 'Хорошо'),
    (3, 'Удовлетворительно'),
    (2, 'Плохо'),
]

LIKED_CHOICES = [
    ('diagnostic', 'Диагностика'),
    ('sound', 'Постановка звуков'),
    ('message', 'Логопедический массаж'),
    ('speech', 'Развитие речи'),
    ('school', 'Подготовка к школе'),
    ('other', 'Другое')
    ]
AGE_CHOICES = [
    ('3-4', '3-4 года'),
    ('4-5', '4-5 лет'),
    ('5-6', '5-6 лет'),
    ('6-7', '6-7 лет'),
    ('7+', 'Старше 7 лет'),
    ]

"""
class Review(models.Model):
    name = models.CharField(
        max_length=100, verbose_name='Имя'
    )
    email = models.EmailField( 
        verbose_name='Email' 
    )
    comment = models.TextField(
        verbose_name='Отзыв'
    ) 
    rating = models.IntegerField(choices=RATING_CHOICES, verbose_name ='Оценка работы')
    liked = models.CharField(max_length = 200, blank = True, choices = LIKED_CHOICES, verbose_name= 'Что понравилось') 
    
    consent = models.BooleanField(
        default=False,
        verbose_name='Согласие на обработку'
    )
    age = models.CharField(max_length = 50, blank = True, choices = AGE_CHOICES, verbose_name = 'Возраст ребёнка')
"""

class Blog(models.Model):
    title = models.CharField(max_length=100, unique_for_date = "posted", verbose_name="Заголовок")
    description = models.TextField(verbose_name="Краткое содержание")
    content = models.TextField(verbose_name="Полное содержание")
    posted = models.DateTimeField(default=datetime.now, db_index = True, verbose_name= "Опубликована")
    author = models.ForeignKey(User, null = True, blank = True, on_delete = models.SET_NULL, verbose_name="Автор")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blogpost", args=[str(self.id)])

    class Meta:
        db_table = "Posts"
        ordering = ["-posted"]
        verbose_name = "статья блога"
        verbose_name_plural = "cтатья блога"

class Comment(models.Model):
    text = models.TextField(verbose_name="Полное содержание")
    create_at = models.DateTimeField(default=datetime.now, db_index = True, verbose_name= "Дата добавления")
    author = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="Автор")
    post = models.ForeignKey(Blog, on_delete=models.CASCADE, verbose_name="Статья")

    class Meta:
        ordering = ["-create_at"]
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

admin.site.register(Blog)
admin.site.register(Comment)