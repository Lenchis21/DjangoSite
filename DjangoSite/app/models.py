from pyexpat import model
from tabnanny import verbose
from turtle import mode
from unicodedata import category
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

class Blog(models.Model):
    title = models.CharField(max_length=100, unique_for_date = "posted", verbose_name="Заголовок")
    description = models.TextField(verbose_name="Краткое содержание")
    content = models.TextField(verbose_name="Полное содержание")
    posted = models.DateTimeField(default=datetime.now, db_index = True, verbose_name= "Опубликована")
    author = models.ForeignKey(User, null = True, blank = True, on_delete = models.SET_NULL, verbose_name="Автор")
    image = models.FileField(default = 'temp.jpg', verbose_name = "Путь к картинке")

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


class ServiceCategory(models.Model):
    """Категория услуг логопеда """
    name = models.CharField("Название категории",max_length=100)
    description = models.TextField(verbose_name ="Описание", blank=True)

    class Meta:
        verbose_name = "Категория услуги"
        verbose_name_plural = "Категории услуг"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_services', args=[str(self.id)]) 

class Service(models.Model):
    """Услуги логопеда"""
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, 
                                 verbose_name="Категория", 
                                 related_name='services')
    name = models.CharField("Название услуги", max_length=100)
    short_description = models.TextField("Краткое описание")
    description = models.TextField("Полное описание")
    price = models.DecimalField(verbose_name="Цена", 
                                max_digits=10,
                                decimal_places=2,
                                blank=True, 
                                help_text="Можно оставить пустым, если услуга бесплатная",
                                null=True)
    image = models.FileField(verbose_name = "Путь к картинке", blank=True)
    duration = models.CharField("Длительность", max_length=100, blank=True)
    age_group = models.CharField("Возрастная группа", max_length=100, blank = True)

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"
        ordering = ['category','name']
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('service_detail', args=[str(self.id)])

admin.site.register(ServiceCategory)
admin.site.register(Service)
admin.site.register(Blog)
admin.site.register(Comment)