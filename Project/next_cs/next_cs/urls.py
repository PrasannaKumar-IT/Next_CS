# next_cs/urls.py
from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),  # Home page
    path('about/', views.about, name='about'),  # About page
    path('contact/', views.contact, name='contact'),  # Contact page
    path('login/', views.login, name='login'),  # login page
    path('register/', views.register, name='register'),
     path('profile/', views.profile_setup, name='profile_setup'), # profile_setup page
    path('dashboard/', views.dashboard, name='dashboard'), # dashboard page
    path('logout/', views.logout_view, name='logout'), # logout page
]
