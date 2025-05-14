from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout,get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.contrib.auth.models import User
import requests
import sys
import json
import random
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from reportlab.lib.pagesizes import letter
from django.db.models import Q
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.http import HttpResponse
from xhtml2pdf import pisa
from .models import CustomUser, Message, UserConnection,ConnectionRequest,Resume, QuizScore
User = get_user_model()  

def home(request):
    return render(request, 'home.html')

def contact(request):
    return render(request, 'contact.html')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'register.html')

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken.")
            return render(request, 'register.html')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return render(request, 'register.html')

        user = CustomUser.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, "Registration successful! You can now log in.")
        return redirect('login')  

    return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, "Login successful!")

            if user.profile_completed:
                return redirect('dashboard')  
            else:
                return redirect('profile_setup')
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'login.html')

def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.is_staff:
            auth_login(request, user)
            messages.success(request, "Admin login successful!")
            return redirect('admin_dashboard')
        else:
            messages.error(request, "Invalid credentials or unauthorized access.")
            
    return render(request, 'admin_login.html')

def is_admin(user):
    return user.is_authenticated and user.is_staff  # Ensures only staff users can access

@login_required
def profile_setup(request):
    if request.user.profile_completed:
        return redirect('dashboard') 

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

        
        selected_skills = request.POST.getlist("skills")
        other_skills = request.POST.get("other_skills", "").strip()
        user.skills = ", ".join(selected_skills + ([other_skills] if other_skills else []))

        if request.FILES.get("profile_picture"):
            user.profile_picture = request.FILES.get("profile_picture")

        user.profile_completed = True
        user.save()

        messages.success(request, "Profile setup complete! Redirecting to Dashboard.")
        return redirect("dashboard")

    return render(request, "profile.html")

@login_required
def dashboard(request):
    user = request.user 
    profile_pic_url = user.profile_picture.url if user.profile_picture else "/static/image/default_profile_pic.jpg"

    if request.FILES.get("profile_picture"):
        user.profile_picture = request.FILES.get("profile_picture")
        user.save()  

    skills = user.skills.split(", ") if user.skills else []
    recommended_learning = [
        {"skill": skill, "description": f"Explore courses & projects in {skill}"} for skill in skills
    ]

    quiz_scores = QuizScore.objects.filter(user=user)
    quiz_data = {quiz.language: quiz.score for quiz in quiz_scores} if quiz_scores.exists() else {}

    job_details = []
    try:
        response = requests.get("https://remoteok.io/api")
        if response.status_code == 200:
            job_data = response.json()[1:11]  
            for job in job_data:
                job_details.append({
                    "title": job.get("position", "Unknown Role"),
                    "company": job.get("company", "Unknown Company"),
                    "salary": job.get("salary", "Not Disclosed"),
                    "type": job.get("tags", ["Full-Time"])[0]  
                })
    except Exception as e:
        print("Job API Error:", str(e), file=sys.stderr)
        job_details = []  

    language_trends = {}
    try:
        response = requests.get("https://api.github.com/search/repositories?q=stars:>500&sort=stars&order=desc")
        if response.status_code == 200:
            repo_data = response.json().get("items", [])[:50]  
            for repo in repo_data:
                lang = repo.get("language", "Unknown")
                if lang and lang != "Unknown":
                    language_trends[lang] = language_trends.get(lang, 0) + 1  

        if language_trends:
            total_repos = sum(language_trends.values())
            sorted_languages = {lang: round((count / total_repos) * 100, 2) for lang, count in language_trends.items()}
            sorted_languages = dict(sorted(sorted_languages.items(), key=lambda x: x[1], reverse=True)[:10])  # Top 10
        else:
            sorted_languages = {}

    except Exception as e:
        print("Language API Error:", str(e), file=sys.stderr)
        sorted_languages = {}

    if not sorted_languages:
        sorted_languages = {"Python": 30, "JavaScript": 25, "C++": 15, "Java": 10, "Go": 8, "Rust": 7, "Swift": 5, "Kotlin": 4}

    language_labels_json = json.dumps(list(sorted_languages.keys()))
    language_percentages_json = json.dumps(list(sorted_languages.values()))

    print("Fetched Programming Languages:", sorted_languages, file=sys.stderr)  # Debugging

    user_data = {
        "username": user.username,
        "profile_pic": profile_pic_url,
        "quiz_scores": quiz_data,
        "skills": skills,
        "recommended_learning": recommended_learning,
        "job_details": job_details,
        "language_labels": language_labels_json,
        "language_percentages": language_percentages_json,
    }

    return render(request, "dashboard.html", {"user_data": user_data})

@login_required
def learning_hub(request):
    user = request.user  
    profile_pic_url = user.profile_picture.url if user.profile_picture else "/static/image/default profile pic.jpg"
    user_data = {
        "username": user.username,
        "profile_pic": profile_pic_url,
    } 
    return render(request, 'learning.html',{"user_data": user_data})

@login_required
def admin_dashboard(request):
    total_users = User.objects.count()  # ✅ Now using core.CustomUser
    applications = random.randint(50, 150)  # Placeholder for total applications
    growth_rate = random.uniform(5, 20)  # Placeholder for growth rate
    usage = random.randint(1000, 5000)  # Placeholder for usage sessions

    context = {
        'total_users': total_users,
        'applications': applications,
        'growth_rate': round(growth_rate, 2),
        'usage': usage
    }
    return render(request, 'admin_dashboard.html', context)

@login_required
def user_growth_chart(request):
    """Generate user growth data for the past 6 months."""
    labels = []
    data = []

    for i in range(6):
        month = datetime.now() - timedelta(days=30 * i)
        labels.append(month.strftime('%b'))  # Month name
        data.append(User.objects.filter(date_joined__month=month.month).count())  # ✅ Now using core.CustomUser

    return JsonResponse({'labels': labels[::-1], 'data': data[::-1]}) 

@login_required
def admin_logout(request):
    logout(request)
    return redirect('admin_login')
@login_required
def job_search(request):
    url = "https://jsearch.p.rapidapi.com/search"
    headers = {
        "X-RapidAPI-Key": "2ad7f2b383msh67846609d0cc1c2p19b334jsnc560b5ad4036",  # Replace with your actual API key
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }

    # Corrected query for all CS-related jobs in India
    query = "Computer Science Jobs in India"

    params = {
        "query": query,
        "country": "IN",  # ✅ FIXED: Use correct country code for India
        "page": "4",
        "num_pages": "6",
        "language": "en"
    }

    response = requests.get(url, headers=headers, params=params)

    # Check API response status
    if response.status_code != 200:
        print(f"API Error: {response.status_code} - {response.text}")
        return render(request, "job_search.html", {"jobs": [], "unique_locations": [], "unique_job_roles": []})

    # Extract jobs from response
    jobs = response.json().get("data", [])

    job_list = []
    locations = set()
    job_roles = set()

    for job in jobs:
        # Get location safely
        location = job.get("job_city", "").strip() if job.get("job_city") else "Location Not Provided"
        locations.add(location)

        # Get job title safely
        job_title = job.get("job_title", "").strip() if job.get("job_title") else "Unknown Role"
        job_roles.add(job_title)

        job_list.append({
            "job_title": job_title,
            "company_name": job.get("employer_name", "Unknown Company"),
            "location": location,
            "job_apply_link": job.get("job_apply_link", "#")
        })

    user = request.user  
    profile_pic_url = user.profile_picture.url if user.profile_picture else "/static/image/default profile pic.jpg"
    user_data = {
        "username": user.username,
        "profile_pic": profile_pic_url,
    } 


    return render(request, "job_search.html", {
        "jobs": job_list,
        "unique_locations": sorted(locations),
        "unique_job_roles": sorted(job_roles),
        "user_data": user_data
    })

@login_required
def save_resume(request):
    if request.method == 'POST':
        resume = Resume(
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            address=request.POST.get('address'),

            # Education
            school_name=request.POST.get('school_name'),
            school_percentage=request.POST.get('school_percentage'),
            school_year=request.POST.get('school_year'),

            college_name=request.POST.get('college_name'),
            college_percentage=request.POST.get('college_percentage'),
            college_year=request.POST.get('college_year'),

            # Projects
            project_title_1=request.POST.get('project_title_1'),
            project_description_1=request.POST.get('project_description_1'),
            project_title_2=request.POST.get('project_title_2'),
            project_description_2=request.POST.get('project_description_2'),

            # Certifications
            certification_1=request.POST.get('certification_1'),
            certification_2=request.POST.get('certification_2'),

            # Skills
            skills=request.POST.get('skills'),
            soft_skills=request.POST.get('soft_skills'),
            languages=request.POST.get('languages'),

            # Photo
            profile_pic=request.FILES.get('photo'),
        )
        resume.save()
        return redirect('template_selection', resume_id=resume.id)
    return render(request, 'resume_builder.html')

@login_required
def resume_builder(request):
    user = request.user  
    profile_pic_url = user.profile_picture.url if user.profile_picture else "/static/image/default profile pic.jpg"
    user_data = {
        "username": user.username,
        "profile_pic": profile_pic_url,
    } 
    return render(request, 'resume_builder.html' ,{"user_data": user_data})

@login_required
def template_selection(request, resume_id):
    resume = Resume.objects.get(id=resume_id)
    user = request.user  
    profile_pic_url = user.profile_picture.url if user.profile_picture else "/static/image/default profile pic.jpg"
    user_data = {
        "username": user.username,
        "profile_pic": profile_pic_url,
    } 
    return render(request, 'template_selection.html', {'resume': resume,"user_data": user_data})
@login_required

def generate_resume_pdf(request):
    if request.method == 'POST':
        template_id = request.POST.get('template_id')
        latest_resume = Resume.objects.last()

        if not latest_resume:
            return HttpResponse("No resume found.")

        template_name = f"resume_templates/template{template_id}.html"
        html_content = render_to_string(template_name, {'resume': latest_resume})

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename=resume_template_{template_id}.pdf'

        pisa_status = pisa.CreatePDF(html_content, dest=response)
        if pisa_status.err:
            return HttpResponse('Error while generating PDF')
        return response

    return redirect('resume_builder')  # fallback if GET
@login_required

def new_connections_view(request):
    users = User.objects.exclude(id=request.user.id)
    # Search logic (optional)
    query = request.GET.get("q")
    if query:
        users = users.filter(username__icontains=query) | users.filter(email__icontains=query)

    # Fetch incoming requests
    incoming_requests = ConnectionRequest.objects.filter(receiver=request.user, status="pending")

    # Fetch outgoing requests
    pending_requests = ConnectionRequest.objects.filter(sender=request.user, status="pending")
    pending_receiver_ids = list(pending_requests.values_list("receiver_id", flat=True))
    connected_user_ids = list(
    UserConnection.objects.filter(user=request.user).values_list("connection_id", flat=True)
)
    user = request.user  
    profile_pic_url = user.profile_picture.url if user.profile_picture else "/static/image/default profile pic.jpg"
    user_data = {
        "username": user.username,
        "profile_pic": profile_pic_url,
    } 
    context = {
        "users": users,
        "pending_receiver_ids": pending_receiver_ids,
        "incoming_requests": incoming_requests,
        "connected_user_ids": connected_user_ids,
        'user_data': user_data
    }
    return render(request, "new_connections.html", context)
@login_required

def send_request_view(request, user_id):
    receiver = get_object_or_404(CustomUser, id=user_id)
    # Check if already sent
    if not ConnectionRequest.objects.filter(sender=request.user, receiver=receiver).exists():
        ConnectionRequest.objects.create(sender=request.user, receiver=receiver)
    return redirect('new-connections')
@login_required

def handle_request_view(request, request_id, action):
    conn_request = get_object_or_404(ConnectionRequest, id=request_id, receiver=request.user)
    if action == "accept":
        conn_request.status = "accepted"
        conn_request.save()
        # Create UserConnection
        from .models import UserConnection
        UserConnection.objects.create(user=conn_request.sender, connection=conn_request.receiver)
        UserConnection.objects.create(user=conn_request.receiver, connection=conn_request.sender)
    elif action == "reject":
        conn_request.status = "rejected"
        conn_request.save()
    return redirect('new-connections')
@login_required

def accept_connection_request(request, request_id):
    connection_request = get_object_or_404(ConnectionRequest, id=request_id, receiver=request.user)

    if connection_request.status == 'pending':
        connection_request.status = 'accepted'
        connection_request.save()

        # Create mutual UserConnection records
        UserConnection.objects.create(user=connection_request.sender, connection=connection_request.receiver)
        UserConnection.objects.create(user=connection_request.receiver, connection=connection_request.sender)

    return redirect('new-connections')  # or use your actual connection page URL name
@login_required

def reject_connection_request(request, request_id):
    connection_request = get_object_or_404(ConnectionRequest, id=request_id, receiver=request.user)

    if connection_request.status == 'pending':
        connection_request.status = 'rejected'
        connection_request.save()

    return redirect('new-connections')  # or use your actual connection page URL name

@login_required
def chat_view(request, user_id=None):
    current_user = request.user
    user = request.user  
    profile_pic_url = user.profile_picture.url if user.profile_picture else "/static/image/default profile pic.jpg"
    user_data = {
        "username": user.username,
        "profile_pic": profile_pic_url,
    } 
    # Get connected users
    connections = UserConnection.objects.filter(user=current_user).values_list('connection', flat=True)
    connected_users = CustomUser.objects.filter(id__in=connections)

    selected_user = None
    messages = []

    if user_id:
        selected_user = get_object_or_404(CustomUser, id=user_id)
        if selected_user.id in connections:
            # Get messages between users
            messages = Message.objects.filter(
                (Q(sender=current_user, receiver=selected_user) |
                 Q(sender=selected_user, receiver=current_user))
            )

    if request.method == 'POST' and selected_user:
        content = request.POST.get('message')
        if content:
            Message.objects.create(sender=current_user, receiver=selected_user, content=content)
            return redirect('chat', user_id=selected_user.id)

    context = {
        'connected_users': connected_users,
        'selected_user': selected_user,
        'messages': messages,
        'user_data': user_data
    }
    
    return render(request, 'chat.html',context)

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')

from django.shortcuts import render, redirect
from .models import QuizCategory, QuizQuestion
from django.contrib.auth.decorators import login_required
from .models import UserQuizHistory

@login_required
def quiz_categories_view(request):
    user = request.user  
    profile_pic_url = user.profile_picture.url if user.profile_picture else "/static/image/default profile pic.jpg"
    user_data = {
        "username": user.username,
        "profile_pic": profile_pic_url,
    }
    categories = QuizCategory.objects.all()
    return render(request, 'quiz_categories.html', {'categories': categories,"user_data": user_data})

@login_required
def start_quiz_view(request, category_id):
    category = get_object_or_404(QuizCategory, id=category_id)
    questions = QuizQuestion.objects.filter(category=category)
    user = request.user  
    profile_pic_url = user.profile_picture.url if user.profile_picture else "/static/image/default profile pic.jpg"
    user_data = {
        "username": user.username,
        "profile_pic": profile_pic_url,
    } 
    if request.method == 'POST':
        score = 0
        total = questions.count()
        for q in questions:
            selected = request.POST.get(str(q.id))
            if selected == q.correct_option:
                score += 1

        # Save to history
        UserQuizHistory.objects.create(
            user=request.user,
            category=category,
            score=score,
            total_questions=total
        )

        # Basic recommendation logic
        if score < total * 0.5:
            suggestion_text = f"You might want to review {category.name} basics."
            suggestion_url = f"/learn/?topic={category.name}"  # Link to your Learning Platform
        else:
            suggestion_text = f"Great job! You can try more advanced topics in {category.name}."
            suggestion_url = f"/learn/?topic={category.name}"
        
        return render(request, 'quiz_result.html', {
            'category': category,
            'score': score,
            'total': total,
            'suggestion_text': suggestion_text,
            'suggestion_url': suggestion_url,
            'user_data': user_data,
        })

    return render(request, 'quiz_questions.html', {
        'category': category,
        'questions': questions,
        'user_data': user_data
    })

@login_required
def quiz_history(request):
    user = request.user  
    profile_pic_url = user.profile_picture.url if user.profile_picture else "/static/image/default profile pic.jpg"
    user_data = {
        "username": user.username,
        "profile_pic": profile_pic_url,
    } 
    history = UserQuizHistory.objects.filter(user=request.user).order_by('-date_taken')
    return render(request, 'quiz_history.html', {'history': history,'user_data': user_data})
