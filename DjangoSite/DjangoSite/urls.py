"""
Definition of urls for DjangoSite.
"""

from datetime import datetime
from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views

from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings


urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('link/', views.link, name='link'),
    path('pool/', views.pool, name='pool'),
    path('blog/', views.blog, name='blog'),
    path('registration/', views.registration, name='registration'),
    path('blogpost/<int:parametr>/', views.blogpost, name='blogpost'),
    path('newpost', views.newpost, name = 'newpost'),
    path('videopost', views.videopost, name = 'videopost'),
    path('catalog', views.catalog, name='catalog'),
    path('category/<int:category_id>/', views.category_services, name='category_services'),
    path('service/<int:service_id>/', views.service_detail, name='service_detail'), 

    path('add-category/', views.add_category, name='add_category'),
    path('add-service/', views.add_service, name='add_service'),
    path('login/',
         LoginView.as_view
         (
             template_name='app/auth/login.html',
             authentication_form=forms.BootstrapAuthenticationForm,
             extra_context=
             {
                 'title': 'Вход',
                 'year' : datetime.now().year,
             }
         ),
         name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('admin/', admin.site.urls),

    path('cart/', views.cart_view, name='cart_view'),
    path('cart/add/<int:service_id>/', views.cart_add, name='cart_add'),
    path('cart/update/<int:item_id>/', views.cart_update, name='cart_update'),
    path('cart/remove/<int:item_id>/', views.cart_remove, name='cart_remove'),
    path('cart/checkout/', views.cart_checkout, name='cart_checkout'),
    path('cart/update_all/', views.cart_update_all, name='cart_update_all'),
    path('myorders/', views.my_orders, name='my_orders'),
    path('manage/orders/', views.orders_manage, name='orders_manage'),
    path('manage/orders/<int:order_id>/done/', views.order_done, name='order_done'),

    path('manage/orders/update/<int:order_id>/', views.order_update_status, name='order_update_status'),

    path('manage/orders/edit-item/<int:item_id>/', views.order_edit_item, name='order_edit_item'),
    path('manage/orders/add-item/<int:order_id>/', views.order_add_item, name='order_add_item'),


    path('editpost/<int:parametr>/', views.edit_blogpost, name='edit_blogpost'),
    path('deletepost/<int:parametr>/', views.delete_blogpost, name='delete_blogpost'),

    # Управление каталогом
    path('admin-panel/news/', views.admin_blog, name='admin_blog'), 

    path('admin-panel/catalog/', views.admin_catalog, name='admin_catalog'),
    path('admin-panel/catalog/edit-category/<int:category_id>/', views.edit_category, name='edit_category'),
    path('admin-panel/catalog/delete-category/<int:category_id>/', views.delete_category, name='delete_category'),
    path('admin-panel/catalog/edit-service/<int:service_id>/', views.edit_service, name='edit_service'),
    path('admin-panel/catalog/delete-service/<int:service_id>/', views.delete_service, name='delete_service'),

    path('admin-panel/users/', views.admin_users, name='admin_users'),
    path('admin-panel/users/<int:user_id>/role/', views.change_user_role, name='change_user_role'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
