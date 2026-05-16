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
    path('add-category/', views.add_category, name='add_category'),
    path('service/<int:service_id>/', views.service_detail, name='service_detail'), 
    path('add-service/', views.add_service, name='add_service'),
    path('login/',
         LoginView.as_view
         (
             template_name='app/login.html',
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
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
