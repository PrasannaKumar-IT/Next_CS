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
    path("resume_builder/", views.resume_builder, name="resume_builder"),
    path("save_resume/", views.save_resume, name="save_resume"),
    path('template_selection/<int:resume_id>/', views.template_selection, name='template_selection'),
    path('generate-pdf/', views.generate_resume_pdf, name='generate_resume_pdf'),
    path('connect/', views.new_connections_view, name='new-connections'),
    path('connect/send/<int:user_id>/', views.send_request_view, name='send-request'),
    path('connect/request/<int:request_id>/<str:action>/', views.handle_request_view, name='handle-request'),
    path('accept-request/<int:request_id>/', views.accept_connection_request, name='accept-request'),
    path('reject-request/<int:request_id>/', views.reject_connection_request, name='reject-request'),
    path('connect/messages/', views.chat_view, name='chat-home'),
    path('connect/messages/<int:user_id>/', views.chat_view, name='chat'),
    path('quiz/', views.quiz_categories_view, name='quiz_categories'),
    path('quiz/<int:category_id>/', views.start_quiz_view, name='start_quiz'),
    path('quiz/history/', views.quiz_history, name='quiz_history'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
