"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpRequest
from django.contrib.auth.decorators import user_passes_test
from .forms import BlogForm, BootstrapRegistrationForm, ReviewForm, CommentForm, ServiceForm, ServicesCategoryForm, QuantityForm
from .models import Blog, ServiceCategory, Comment, Service, Order, OrderItem
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

def home(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Главная страница',
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
    return render(request, 'app/services/pool.html', {
        'form': form,
        'data': data,
        'title':title
    })

def registration(request):
    if request.method == "POST":
        regform = BootstrapRegistrationForm(request.POST) 
        if regform.is_valid():
            reg_f = regform.save(commit=False)
            reg_f.is_staff = False
            reg_f.is_active = True
            reg_f.is_superuser = False
            reg_f.save()
            return redirect('home')
    else:
        regform = BootstrapRegistrationForm()
        
    return render(
        request,
        'app/auth/registration.html',
        {
            'regform': regform,
            'year': datetime.now().year,
        }
    )

def blog(request):
    """Renders the blog page."""
    assert isinstance(request, HttpRequest)
    posts = Blog.objects.all()
    return render(
        request,
            'app/blog/blog.html',
            {
                'title':'Блог',
                'posts': posts,
                'year': datetime.now().year,
            }        
        
        )
def blogpost(request, parametr):
    """ Renders the blogpost page. """
    assert isinstance(request, HttpRequest)
    post_1 = Blog.objects.get(id=parametr)
    comments = Comment.objects.filter(post=parametr)
    
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_f = form.save(commit=False)
            comment_f.author = request.user
            comment_f.date = datetime.now()
            comment_f.post = post_1
            comment_f.save()
            return redirect('blogpost', parametr=post_1.id)
    else:
        form = CommentForm()

    return render(
        request,
        'app/blog/blogpost.html',
        {
            'post_1': post_1,
            'year': datetime.now().year,
            'comments': comments,
            'form': form,
        }
    )
def newpost(request):
    assert isinstance(request, HttpRequest)

    if request.method == "POST":
        blogform = BlogForm(request.POST, request.FILES)
        if blogform.is_valid():
            blog_f = blogform.save(commit=False)
            blog_f.posted = datetime.now()
            blog_f.author = request.user
            blog_f.save()

            return redirect('blog')
    else:
        blogform = BlogForm()


    return render(
        request,
        'app/blog/newpost.html',
            {
                'blogform': blogform,
                'title': 'Добавить статью блога',

                'year': datetime.now().year,
            }
        )
def videopost(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/blog/videopost.html',
        {
            'title':'Видео',
        })

def catalog(request):
    """Страница каталога услуг"""
    categories = ServiceCategory.objects.all()
    return render(request, 'app/services/catalog.html', {
        'categories': categories,
        'title': 'Каталог услуг'
    })

def category_services(request, category_id):
    """Список услуг в выбранной категории"""
    category = get_object_or_404(ServiceCategory, id=category_id)
    services = Service.objects.filter(category=category)
    return render(request, 'app/services/category_services.html', {
            'category':category,
            'services':services
        })
def service_detail(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    return render(request, 'app/services/service_detail.html', {'service': service})


@user_passes_test(lambda u: u.is_superuser)
def add_category(request):
    if request.method == 'POST':
        form = ServicesCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('catalog')
    else:
        form = ServicesCategoryForm()
    return render(request, 'app/services/add_category.html', {'form': form, 'title': 'Добавить категорию'})


@user_passes_test(lambda u: u.is_superuser)
def add_service(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('catalog')
    else:
        form = ServiceForm()
    return render(request, 'app/services/add_service.html', {'form': form, 'title': 'Добавить услугу'})


# --- Корзина ----

def get_cart(request):
    """Возвращает текущую корзину пользователя, создавая её при необходимости."""
    cart, created = Order.objects.get_or_create(
        customer=request.user, status='cart'
    )
    return cart

@login_required
def cart_add(request, service_id):
    """Добавление услуги в корзину (сразу по 1 шт.)"""
    service = get_object_or_404(Service, id=service_id)
    cart = get_cart(request)
    
    # Ищем, есть ли уже эта услуга в корзине
    item, created = OrderItem.objects.get_or_create(
        order=cart, service=service,
        defaults={'quantity': 1}
    )
    
    # Если услуга уже была, просто прибавляем 1
    if not created:
        item.quantity += 1
        item.save()
        
    return redirect('cart_view')

@login_required
def cart_view(request):
    """Просмотр корзины."""
    cart = get_cart(request)
    items = cart.orderitem_set.all()
    return render(request, 'app/cart/cart.html', {
        'cart': cart, 'items': items, 'total': cart.total(),
        'year': datetime.now().year,
    })

@login_required
def cart_update(request, item_id):
    """Изменение количества занятий в корзине."""
    item = get_object_or_404(OrderItem, id=item_id, order__customer=request.user)
    form = QuantityForm(request.POST or None, initial={'quantity': item.quantity})
    if request.method == "POST" and form.is_valid():
        item.quantity = form.cleaned_data['quantity']
        item.save()
        return redirect('cart_view')
    return render(request, 'app/cart/cart_update.html', {
        'form': form, 'item': item, 'year': datetime.now().year,
    })

@login_required
def cart_update_all(request):
    """Сохранение всех изменений количеств из корзины"""
    if request.method == "POST":
        cart = get_cart(request)
        items = cart.orderitem_set.all()
        
        # Проходимся по всем товарам в корзине
        for item in items:
            # Достаем количество из POST-запроса по имени поля
            new_qty = request.POST.get(f'quantity_{item.id}')
            if new_qty is not None:
                try:
                    new_qty = int(new_qty)
                    if new_qty > 0:
                        item.quantity = new_qty
                        item.save()
                    else:
                        item.delete() # Если ввели 0, удаляем
                except ValueError:
                    pass # Игнорируем, если ввели не число
                    
    return redirect('cart_view')

@login_required
def cart_remove(request, item_id):
    """Удаление позиции из корзины."""
    item = get_object_or_404(OrderItem, id=item_id, order__customer=request.user)
    item.delete()
    return redirect('cart_view')

@login_required
def cart_checkout(request):
    """Оформление заказа: корзина становится заказом."""
    cart = get_cart(request)
    if request.method == "POST":
        comment = request.POST.get('comment', '')
        if comment:
            cart.comment = comment
        cart.status = 'new'
        cart.save()
        return redirect('my_orders')
    return render(request, 'app/cart/checkout.html', {
        'cart': cart, 'total': cart.total(), 'year': datetime.now().year,
    })

@login_required
def my_orders(request):
    """История заказов клиента."""
    orders = Order.objects.filter(customer=request.user).exclude(status='cart')
    return render(request, 'app/cart/my_orders.html', {
        'orders': orders, 'year': datetime.now().year,
    })


@staff_member_required
def orders_manage(request):
    """Управление заказами для менеджера."""
    orders = Order.objects.exclude(status='cart').order_by('-date')
    return render(request, 'app/cart/orders_manage.html', {
        'orders': orders, 'year': datetime.now().year,
    })


@staff_member_required
def order_done(request, order_id):
    """Отметить заказ выполненным."""
    order = get_object_or_404(Order, id=order_id)
    order.status = 'done'
    order.save()
    return redirect('orders_manage')