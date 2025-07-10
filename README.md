
# Next-CS: A Comprehensive Career Guidance Platform for CS Students

## 🧭 Overview

**Next-CS** is a web-based career guidance platform tailored for Computer Science (CS) students and fresh graduates. It aims to bridge the gap between academic learning and career readiness by offering personalized learning paths, real-time job listings, quizzes for self-assessment, resume building, and a social networking space for peer collaboration.

Built using **Django** on the backend and **HTML, CSS, JavaScript** on the frontend, the platform integrates multiple free APIs to deliver a centralized and enriched career development experience.

---

## 📌 Features

- 🎯 **Personalized Career Dashboard**
- 🧪 **Quiz Hub** with topic/language-based MCQs
- 📚 **Learning Paths & Resource Suggestions**
- 💼 **Live Job Listings** via APIs (RemoteOK, GitHub Jobs, JSearch)
- 📄 **Resume Builder** with multiple templates and PDF download
- 🧑‍🤝‍🧑 **Connect Campus** for peer networking and chat
- 🛠️ **Admin Panel** for platform management

---

## 🎯 Objectives

- Provide tailored career recommendations based on skills and interests.
- Assist in job discovery through real-time API integration.
- Support continuous learning via curated content and structured roadmaps.
- Enable users to build and download professional resumes.
- Foster community interaction through chat and connection features.
- Offer centralized dashboards to monitor learning and job trends.

---

## 🧩 Modules Breakdown

| Module               | Description |
|----------------------|-------------|
| **User Authentication** | Secure login/logout, email validation |
| **Profile Setup**        | Collects user interests, education, skills, etc. |
| **Dashboard**            | Visual summary of jobs, activities, learning paths |
| **Quiz Hub**             | Topic/language quizzes with score tracking |
| **Learning Platform**    | External resource links + personalized roadmaps |
| **Resume Builder**       | Input details, choose template, generate PDF |
| **Job Search**           | Fetch job listings via APIs with filters |
| **Connect Campus**       | Peer discovery, friend requests, live chat |
| **Admin Dashboard**      | Manage users, data, and platform content |

---


### 💾 Software Requirements

| Software | Details |
|---------|---------|
| Backend | Django (Python) |
| Frontend | HTML5, CSS3, JavaScript, Bootstrap |
| Database | MySQL |
| APIs | GitHub Jobs, RemoteOK, JSearch |
| Tools | Django REST Framework, ReportLab, Pillow, WeasyPrint |
| IDE | VS Code|

---

## 🔁 Software Architecture

**MVC Pattern (Model-View-Controller):**
- **Model** – Manages data (users, quizzes, resumes, chats, etc.)
- **View** – HTML/CSS templates render UI
- **Controller** – Django views and logic handle routing and operations

---

## 📂 Project Structure (Simplified)

```bash
next_cs/
├── core/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── templates/
├── static/
│   ├── css/
│   ├── js/
│   └── images/
├── resume/
│   ├── templates/
│   └── pdf_generation/
├── quiz/
│   ├── quiz_views.py
│   └── questions/
├── jobs/
│   ├── api_integrations/
├── connect_campus/
│   ├── chat/
│   └── friends/
├── templates/
├── manage.py
└── requirements.txt
```

---

## 🔗 APIs Used

- [RemoteOK API](https://remoteok.io/api)
- [GitHub Jobs API](https://jobs.github.com/api)
- [JSearch via RapidAPI](https://rapidapi.com)

---

## 🚀 Installation & Setup

### Prerequisites:
- Python 3.8+
- MySQL
- pip (Python Package Installer)
- Git

### Steps:
```bash
# Clone the repo
git clone https://github.com/your-username/next-cs.git
cd next-cs

# Install dependencies
pip install -r requirements.txt

# Set up the database
python manage.py makemigrations
python manage.py migrate

# Create a superuser
python manage.py createsuperuser

# Run the server
python manage.py runserver
```

---

## 📄 PDF Resume Generation Tools

- **ReportLab**: For generating resumes dynamically.
- **WeasyPrint**: Optional tool for converting HTML/CSS to PDF.

---

## 📧 Contact

For any queries or collaboration:

- 📧 Email: [youremail@example.com]
- 🧑‍💻 GitHub: [github.com/yourusername]
- 🌐 Website: [optional]

---

