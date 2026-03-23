from django.db import models

# ПЕРЕНЕСИТЕ СПИСОК СЮДА (уберите отступ слева)
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

class Review(models.Model):
    name = models.CharField(
        max_length=100,  
        verbose_name='Имя'
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
