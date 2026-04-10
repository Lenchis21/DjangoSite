"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest
from .forms import ReviewForm
from django.shortcuts import render, redirect

from django.contrib.auth.forms import UserCreationForm




def home(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Домашняя страница',
            'year':datetime.now().year,
        }
    )

def contact(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Контакты',
            'message':'Ваша страница контактов.',
            'year':datetime.now().year,
        }
    )

def about(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'О нас',
            'message':'Страница описания вашего приложения.',
            'year':datetime.now().year,
        }
    )

def link(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/link.html',
        {
            'title':'Полезные ссылки',
            'message':'Страница описания вашего приложения.',
            'year':datetime.now().year,
        }
    )

def pool(request):
    assert isinstance(request, HttpRequest)
    data = None
    rating = {5 : 'Отлично', 4 : 'Хорошо', 3: 'Удовлетворительно', 2 :'Плохо'}
    liked = {'diagnostic' :'Диагностика',
            'sound': 'Постановка звуков',
            'message' : 'Логопедический массаж',
            'speech': 'Развитие речи', 
            'school' : 'Подготовка к школе', 'other' : 'Другое'}

    age = {'3-4' : '3-4 года', '4-5' : '4-5 лет', '5-6' : '5-6 лет',
            '6-7' : '6-7 лет', '7+' : 'Старше 7 лет'
          }
    title = 'Опрос для родителей'
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            data = dict()
            data['name'] = form.cleaned_data['name']
            data['email'] = form.cleaned_data['email']
            data['rating'] =form.cleaned_data['rating']
            data['liked'] = form.cleaned_data['liked']
            data['age'] = form.cleaned_data['age']
            data['message'] = form.cleaned_data['message']
            data['consent'] = form.cleaned_data['consent']
            
            if form.cleaned_data.get('notice'):
                data['notice'] = 'Да'
            else:
                data['notice'] = 'Нет'

    else:
        form = ReviewForm()
    return render(request, 'app/pool.html', {
        'form': form,
        'data': data,
        'title':title
    })

def registration(request):
    """Renders the registration page."""
    
    if request.method == "POST":                    # после отправки формы
        regform = UserCreationForm(request.POST)
        if regform.is_valid():
            reg_f = regform.save(commit=False)
            reg_f.is_staff = False                 # запрещен вход в административный раздел
            reg_f.is_active = True                  # активный пользователь
            reg_f.is_superuser = False              # не является суперпользователем
            reg_f.date_joined = datetime.now()      # дата регистрации
            reg_f.last_login = datetime.now()       # дата последней авторизации
            
            regform.save()                          # сохраняем изменения после добавления полей
            
            return redirect('home')                 # переадресация на главную страницу после регистрации
    else:
        regform = UserCreationForm()                # создание объекта формы для ввода данных
        
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/registration.html',
        {
            'regform': regform,                     # передача формы в шаблон веб-страницы
            'year': datetime.now().year,
        }
    )





