# next_cs/urls.py
from django.contrib import admin
from django.urls import path
from core import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'), 
    path('about/', views.about, name='about'),  
    path('contact/', views.contact, name='contact'),  
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile_setup, name='profile_setup'), 
    path('dashboard/', views.dashboard, name='dashboard'), 
    path('logout/', views.logout_view, name='logout'),
    path('learning_hub/', views.learning_hub, name='learning_hub'), 
    path('admin_login/', views.admin_login, name='admin_login'), 
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-logout/', views.admin_logout, name='admin_logout'),
    path('user-growth-data/', views.user_growth_chart, name='user_growth_chart'),
    path("job_search/", views.job_search, name="job_search"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
