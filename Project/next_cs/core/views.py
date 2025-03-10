from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import CustomUser  # Use CustomUser instead of User


def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


# ✅ Fixed Registration View (Now Uses `CustomUser`)
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Validate inputs
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'register.html')

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken.")
            return render(request, 'register.html')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return render(request, 'register.html')

        # Create the user
        user = CustomUser.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, "Registration successful! You can now log in.")
        return redirect('login')  # Redirect to login page

    return render(request, 'register.html')


# ✅ Fixed Login View (Redirects New Users to Profile Setup)
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, "Login successful!")

            # Check if profile is completed
            if user.profile_completed:
                return redirect('dashboard')  # Redirect old users to Dashboard
            else:
                return redirect('profile_setup')  # Redirect new users to Profile Setup
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'login.html')


# ✅ Fixed Profile Setup View (Now Saves Data to `CustomUser`)
@login_required
def profile_setup(request):
    if request.user.profile_completed:
        return redirect('dashboard')  # If already completed, go to Dashboard

    if request.method == "POST":
        user = request.user
        user.first_name = request.POST.get("full_name", "").strip()
        user.phone_number = request.POST.get("phone_number", "").strip()
        user.degree = request.POST.get("degree", "").strip()
        user.university = request.POST.get("university", "").strip()
        user.graduation_year = request.POST.get("graduation_year", "").strip()
        user.career_path = request.POST.get("career_path", "").strip()
        user.work_preference = request.POST.get("work_preference", "").strip()
        user.linkedin = request.POST.get("linkedin", "").strip()
        user.github = request.POST.get("github", "").strip()
        user.portfolio = request.POST.get("portfolio", "").strip()

        # Process skills (checkboxes)
        selected_skills = request.POST.getlist("skills")
        other_skills = request.POST.get("other_skills", "").strip()
        user.skills = ", ".join(selected_skills + ([other_skills] if other_skills else []))

        # Handle Profile Picture Upload
        if "profile_picture" in request.FILES:
            user.profile_picture = request.FILES["profile_picture"]

        # Mark profile as completed
        user.profile_completed = True
        user.save()

        messages.success(request, "Profile setup complete! Redirecting to Dashboard.")
        return redirect("dashboard")

    return render(request, "profile.html")



# ✅ Fixed Logout View
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')


# ✅ Fixed Dashboard View
@login_required
def dashboard(request):
    return render(request, 'dashboard.html')
