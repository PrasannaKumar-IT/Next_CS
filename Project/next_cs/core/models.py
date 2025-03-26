from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    degree = models.CharField(max_length=50, choices=[("BSc", "BSc"), ("MSc", "MSc"), ("PhD", "PhD")], blank=True)
    university = models.CharField(max_length=100, blank=True)
    graduation_year = models.IntegerField(blank=True, null=True)
    skills = models.TextField(blank=True, help_text="Comma-separated skills")
    career_path = models.CharField(max_length=100, blank=True)
    work_preference = models.CharField(max_length=50, choices=[("Remote", "Remote"), ("Hybrid", "Hybrid"), ("On-Site", "On-Site")], blank=True)
    linkedin = models.URLField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)
    portfolio = models.URLField(blank=True, null=True)
    profile_completed = models.BooleanField(default=False) 
    is_admin = models.BooleanField(default=False) 

    def __str__(self):
        return self.username


class QuizScore(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    language = models.CharField(max_length=50) 
    score = models.IntegerField() 

    def __str__(self):
        return f"{self.user.username} - {self.language} - {self.score}%"


class UserConnection(models.Model):
    """Model to store user connections (e.g., campus connect)."""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="connections")
    connection = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="followers")
    connected_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} connected with {self.connection.username}"
