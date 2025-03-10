from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    """Custom user model with profile fields."""
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
    profile_completed = models.BooleanField(default=False)  # Track profile completion

    def __str__(self):
        return self.username
