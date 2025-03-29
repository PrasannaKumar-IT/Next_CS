from django.contrib import admin
from .models import CustomUser, QuizScore, UserConnection


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone_number', 'university', 'graduation_year', 'profile_completed', 'is_admin')
    search_fields = ('username', 'email', 'university', 'skills', 'career_path')
    list_filter = ('profile_completed', 'is_admin', 'work_preference', 'degree')
    ordering = ('username',)

@admin.register(QuizScore)
class QuizScoreAdmin(admin.ModelAdmin):
    list_display = ("user", "quiz_name", "score", "date_taken")  # ✅ Ensure correct fields
    list_filter = ("quiz_name", "score")  
    search_fields = ("user__username", "quiz_name")  

@admin.register(UserConnection)
class UserConnectionAdmin(admin.ModelAdmin):
    list_display = ('user', 'connection', 'connected_at')
    search_fields = ('user__username', 'connection__username')
    list_filter = ('connected_at',)

