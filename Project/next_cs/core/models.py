from django.contrib.auth.models import AbstractUser
from django.db import models 
from django.conf import settings 
from django.utils.timezone import now

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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    quiz_name = models.CharField(max_length=255, default="Unknown Quiz")  # ✅ Set default value
    score = models.IntegerField()
    date_taken = models.DateTimeField(default=now)  # Ensure date_taken has a default value

    def __str__(self):
        return f"{self.user.username} - {self.quiz_name} ({self.score})"

class UserConnection(models.Model):
    """Model to store user connections (e.g., campus connect)."""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="connections")
    connection = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="followers")
    connected_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} connected with {self.connection.username}"
    
class ConnectionRequest(models.Model):
    sender = models.ForeignKey(CustomUser, related_name='sent_requests', on_delete=models.CASCADE)
    receiver = models.ForeignKey(CustomUser, related_name='received_requests', on_delete=models.CASCADE)
    status = models.CharField(
        max_length=10,
        choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')],
        default='pending'
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username} -> {self.receiver.username} ({self.status})"

class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']  # Messages ordered chronologically

    def __str__(self):
        return f"{self.sender.username} -> {self.receiver.username} at {self.timestamp}"

class Job(models.Model):
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    url = models.URLField()

    def __str__(self):
        return f"{self.title} at {self.company}"

class Resume(models.Model):
    name = models.CharField(max_length=100,default="[]")
    email = models.EmailField(unique=True,blank=True)
    phone = models.CharField(max_length=20,default="[]")
    address = models.TextField(blank=True,default="[]")
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    school_name = models.CharField(max_length=200,default="[]")
    school_percentage = models.CharField(max_length=10,default="[]")
    school_year = models.CharField(max_length=4,default="[]")
    college_name = models.CharField(max_length=200, default="[]")
    college_percentage = models.CharField(max_length=10,default="[]")
    college_year = models.CharField(max_length=4,default="[]")
    # Project fields (non-JSON)
    project_title_1 = models.CharField(max_length=200, blank=True, null=True)
    project_description_1 = models.TextField(blank=True, null=True)
    project_title_2 = models.CharField(max_length=200, blank=True, null=True)
    project_description_2 = models.TextField(blank=True, null=True)

    # Certifications fields (non-JSON)
    certification_1 = models.CharField(max_length=255, blank=True, null=True)
    certification_2 = models.CharField(max_length=255, blank=True, null=True)
    
    skills = models.TextField(help_text="Comma-separated values",default=" ")
    soft_skills = models.TextField(help_text="Comma-separated values",default=" ")
    languages = models.TextField(help_text="Comma-separated values",default="")
    achievements = models.TextField(blank=True,default="[]")

    def __str__(self):
        return f"{self.name}'s Resume"
    

from django.db import models

class QuizCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.name


class QuizQuestion(models.Model):
    category = models.ForeignKey(QuizCategory, on_delete=models.CASCADE)
    question = models.TextField()
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_option = models.CharField(
        max_length=1,
        choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')]
    )

    def __str__(self):
        return self.question[:60]


from django.db import models
from django.contrib.auth.models import User
from .models import QuizCategory

from django.conf import settings  # 👈 this imports your custom user model reference

class UserQuizHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(QuizCategory, on_delete=models.CASCADE)
    score = models.IntegerField()
    total_questions = models.IntegerField()
    date_taken = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.category.name} ({self.score}/{self.total_questions})"

