
from datetime import datetime
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpRequest
from django.contrib.auth.decorators import user_passes_test
from .forms import BlogForm, BootstrapRegistrationForm, ReviewForm, CommentForm, ServiceForm, ServicesCategoryForm, QuantityForm
from .models import Blog, ServiceCategory, Comment, Service, Order, OrderItem, Review
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User

# ------------------- Информация сайта ----------------------

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
    title = 'Опрос для родителей'
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = Review()
            review.name = form.cleaned_data['name']
            review.email = form.cleaned_data['email']
            review.rating = form.cleaned_data['rating']
            
            liked_list = form.cleaned_data.get('liked', [])
            review.liked = ", ".join(liked_list)
            
            review.age = form.cleaned_data['age']
            review.message = form.cleaned_data['message']
            review.consent = form.cleaned_data['consent']
            review.save()
            
            return render(request, 'app/services/pool.html', {
                'form': ReviewForm(), 
                'title': title, 
                'success': True
            })
    else:
        form = ReviewForm()
        
    return render(request, 'app/services/pool.html', {
        'form': form,
        'title': title
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

def videopost(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/blog/videopost.html',
        {
            'title':'Видео',
        })

# --------------------------------------------------------------------------

# ---------------------------- Блог ----------------------------------------
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

@staff_member_required
def edit_blogpost(request, parametr):
    """Редактирование статьи блога (новости)."""
    if not request.user.is_superuser:
        return redirect('home') 

    post_1 = get_object_or_404(Blog, id=parametr)
    if request.method == "POST":
        blogform = BlogForm(request.POST, request.FILES, instance=post_1)
        if blogform.is_valid():
            blogform.save()
            return redirect('blog')
    else:
        blogform = BlogForm(instance=post_1)
        
    return render(request, 'app/blog/editpost.html', {
        'blogform': blogform,
        'title': 'Редактировать статью',
        'year': datetime.now().year,
    })

@staff_member_required
def delete_blogpost(request, parametr):
    """Удаление статьи блога (новости)."""
    if not request.user.is_superuser:
        return redirect('home')
        
    post_1 = get_object_or_404(Blog, id=parametr)
    post_1.delete()
    return redirect('blog')

# ------------------------------ Услуги ------------------------------

def catalog(request):
    """Страница каталога услуг"""
    categories = ServiceCategory.objects.all()
    return render(request, 'app/services/catalog.html', {
        'categories': categories,
        'title': 'Каталог'
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

# ======================================================================

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

# --------------------------------------------------------------------




# --- Корзина ----

@login_required
def get_cart(request):
    cart, created = Order.objects.get_or_create(
        customer=request.user, status='cart'
    )
    return cart

@login_required
def cart_view(request):
    cart = get_cart(request)
    items = cart.orderitem_set.all()
    return render(request, 'app/cart/cart.html', {
        'cart': cart, 'items': items, 'total': cart.total(),
        'year': datetime.now().year,
    })

@login_required
def cart_add(request, service_id):
    """Добавление услуги в корзину (по 1 шт. за клик)."""
    service = get_object_or_404(Service, id=service_id)
    cart = get_cart(request)
    
    item, created = OrderItem.objects.get_or_create(
        order=cart, service=service,
        defaults={'quantity': 1}
    )
    
    if not created:
        item.quantity += 1
        item.save()
        
    return redirect('cart_view')

@login_required
def cart_update(request, item_id):
    """Изменение количества занятий в корзине (без JS, через перезагрузку)."""
    item = get_object_or_404(OrderItem, id=item_id, order__customer=request.user)
    
    action = request.GET.get('action')

    if action == 'plus':
        item.quantity += 1
        item.save()
    elif action == 'minus':
        if item.quantity > 1:
            item.quantity -= 1
            item.save()
        else:
            item.delete()
            return redirect('cart_view')

    return redirect('cart_view')

@login_required
def cart_update_all(request):
    """Сохранение всех изменений количеств из корзины"""
    if request.method == "POST":
        cart = get_cart(request)
        items = cart.orderitem_set.all()
        
        for item in items:
            new_qty = request.POST.get(f'quantity_{item.id}')
            if new_qty is not None:
                try:
                    new_qty = int(new_qty)
                    if new_qty > 0:
                        item.quantity = new_qty
                        item.save()
                    else:
                        item.delete()
                except ValueError:
                    pass
                    
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


# --------------------- Заказы -------------------------

@login_required
def my_orders(request):
    orders = Order.objects.filter(customer=request.user).exclude(status='cart')
    return render(request, 'app/cart/my_orders.html', {
        'orders': orders, 'year': datetime.now().year,
    })

@staff_member_required
def orders_manage(request):
    orders = Order.objects.exclude(status='cart').order_by('-date')
    services = Service.objects.all()
   
    return render(request, 'app/cart/orders_manage.html', {
        'orders': orders, 
        'services': services,
        'year': datetime.now().year,
    })

@staff_member_required
def order_done(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.status = 'done'
    order.save()
    return redirect('orders_manage')

@staff_member_required
def order_update_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    if request.method == "POST":
        new_status = request.POST.get('status')
        if new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
            order.save()
            
    return redirect('orders_manage')

@staff_member_required
@require_POST
def order_edit_item(request, item_id):
    item = get_object_or_404(OrderItem, id=item_id)
    action = request.POST.get('action')
    
    if action == 'plus':
        item.quantity += 1
        item.save()
    elif action == 'minus':
        if item.quantity > 1:
            item.quantity -= 1
            item.save()
        else:
            item.delete()
    elif action == 'delete':
        item.delete()
        
    return redirect('orders_manage')

@staff_member_required
@require_POST
def order_add_item(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    service_id = request.POST.get('service_id')
    
    if service_id:
        service = get_object_or_404(Service, id=service_id)
        item, created = OrderItem.objects.get_or_create(
            order=order, service=service, defaults={'quantity': 1}
        )
        if not created:
            item.quantity += 1
            item.save()
            
    return redirect('orders_manage')


# --- УПРАВЛЕНИЕ КАТАЛОГОМ (АДМИН) ---

@staff_member_required
def admin_catalog(request):
    """Панель управления каталогом для администратора."""
    if not request.user.is_superuser:
        return redirect('home')
        
    categories = ServiceCategory.objects.all()
    services = Service.objects.all()
    
    return render(request, 'app/admin/catalog_manage.html', {
        'categories': categories,
        'services': services,
        'title': 'Управление каталогом',
        'year': datetime.now().year,
    })

@staff_member_required
def edit_category(request, category_id):
    """Редактирование категории."""
    if not request.user.is_superuser:
        return redirect('home')
        
    category = get_object_or_404(ServiceCategory, id=category_id)
    if request.method == 'POST':
        form = ServicesCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('admin_catalog')
    else:
        form = ServicesCategoryForm(instance=category)
        
    return render(request, 'app/admin/edit_category.html', {
        'form': form, 
        'title': 'Редактировать категорию',
        'year': datetime.now().year,
    })

@staff_member_required
def delete_category(request, category_id):
    """Удаление категории."""
    if not request.user.is_superuser:
        return redirect('home')
        
    category = get_object_or_404(ServiceCategory, id=category_id)
    category.delete()
    return redirect('admin_catalog')

@staff_member_required
def edit_service(request, service_id):
    """Редактирование услуги."""
    if not request.user.is_superuser:
        return redirect('home')
        
    service = get_object_or_404(Service, id=service_id)
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            form.save()
            return redirect('admin_catalog')
    else:
        form = ServiceForm(instance=service)
        
    return render(request, 'app/admin/edit_service.html', {
        'form': form, 
        'title': 'Редактировать услугу',
        'year': datetime.now().year,
    })

@staff_member_required
def delete_service(request, service_id):
    """Удаление услуги."""
    if not request.user.is_superuser:
        return redirect('home')
        
    service = get_object_or_404(Service, id=service_id)
    service.delete()
    return redirect('admin_catalog')

@staff_member_required
def admin_blog(request):
    """Управление новостями (блогом) для администратора."""
    if not request.user.is_superuser:
        return redirect('home')
        
    all_posts = Blog.objects.all().order_by('-posted')
    
    return render(request, 'app/admin/manage_news.html', {
        'all_posts': all_posts, 
        'year': datetime.now().year,
    })

@staff_member_required
def admin_users(request):
    """Список пользователей для управления ролями."""
    if not request.user.is_superuser:
        return redirect('home')
        
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'app/admin/users.html', {'users': users, 'title': 'Пользователи', 'year': datetime.now().year})

@staff_member_required
@require_POST
def change_user_role(request, user_id):
    """Смена роли или удаление пользователя."""
    if not request.user.is_superuser:
        return redirect('home')
        
    user = get_object_or_404(User, id=user_id)
    action = request.POST.get('action')

    if user != request.user: 
        if action == 'make_manager':
            user.is_staff = True
            user.save()
        elif action == 'make_client':
            user.is_staff = False
            user.save()
        elif action == 'delete':
            user.delete()
            return redirect('admin_users')
            
    return redirect('admin_users')