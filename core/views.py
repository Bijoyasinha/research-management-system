from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import login, logout as django_logout, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .models import ResearchPaper, Department
from django.utils import timezone
from datetime import datetime

# --- ড্যাশবোর্ড ---
@login_required
def dashboard(request):
    is_admin = request.user.is_staff or request.user.is_superuser
    
    if is_admin:
        # অ্যাডমিন/টিচার সব পেপার দেখতে পারবে
        papers = ResearchPaper.objects.all().order_by('-submitted_at')
    else:
        # সাধারণ স্টুডেন্ট শুধু তার নিজের পেপার দেখবে
        papers = ResearchPaper.objects.filter(student=request.user).order_by('-submitted_at')

    context = {
        'papers': papers,
        'is_admin': is_admin,
        'departments': Department.objects.all(),
        'approved_count': papers.filter(status='Accepted').count(),
        'pending_count': papers.filter(status='Pending').count(),
        'rejected_count': papers.filter(status='Rejected').count(),
    }
    return render(request, 'dashboard.html', context)

# --- লগইন ভিউ ---
@csrf_exempt
def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST) # 'request' পাস করা জরুরি
        if form.is_valid():
            user = form.get_user()
            login(request, user) # সেশন তৈরি
            return redirect('dashboard')
        else:
            messages.error(request, "ইউজারনেম বা পাসওয়ার্ড ভুল!")
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})

@csrf_exempt
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # রোল সেট করা হচ্ছে
            if user.username == 'Bijoya':
                user.is_staff = True
                user.is_superuser = True
            else:
                user.is_staff = False
                user.is_superuser = False
            
            user.is_active = True  # এটি নিশ্চিত করবে স্টুডেন্ট লগইন করতে পারবে
            user.save()
            
            login(request, user) # সাইনআপের সাথে সাথেই লগইন হয়ে যাবে
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

# --- লগআউট ---
def logout_view(request):
    django_logout(request)
    return redirect('home')

# --- পেপার আপলোড ---
@login_required
def upload_paper(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        dept_id = request.POST.get('department')
        pdf_file = request.FILES.get('pdf_file')
        
        try:
            dept = get_object_or_404(Department, id=int(dept_id))
            
            if dept.deadline and timezone.now() > dept.deadline:
                messages.error(request, "দুঃখিত, এই ডিপার্টমেন্টের ডেডলাইন শেষ হয়ে গেছে।")
                return redirect('upload_paper')
            
            if pdf_file:
                ResearchPaper.objects.create(
                    student=request.user,
                    title=title,
                    department=dept,
                    file=pdf_file
                )
                messages.success(request, "রিসার্চ পেপার সফলভাবে আপলোড হয়েছে!")
                return redirect('dashboard')
        except (ValueError, TypeError):
            messages.error(request, "ডিপার্টমেন্ট সঠিক নয়।")
            
    return render(request, 'upload.html', {'departments': Department.objects.all()})

# --- পেপার রিভিউ (টিচার প্যানেল) ---
@login_required
def review_paper(request, paper_id):
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, "আপনার এই পেজ দেখার অনুমতি নেই।")
        return redirect('dashboard')
        
    paper = get_object_or_404(ResearchPaper, id=paper_id)
    if request.method == 'POST':
        paper.status = request.POST.get('status')
        paper.reviewer_feedback = request.POST.get('feedback')
        paper.save()
        messages.success(request, "রিভিউ আপডেট হয়েছে।")
        return redirect('dashboard')
    return render(request, 'review_paper.html', {'paper': paper})

# --- পেপার ডিলিট ---
@login_required
def delete_paper(request, paper_id):
    paper = get_object_or_404(ResearchPaper, id=paper_id)
    if request.user.is_staff or paper.student == request.user:
        paper.delete()
        messages.success(request, "পেপারটি ডিলিট করা হয়েছে।")
    return redirect('dashboard')

# --- ডেডলাইন আপডেট ---
@login_required
def update_deadline(request, dept_id):
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect('dashboard')

    if request.method == 'POST':
        new_deadline_str = request.POST.get('new_deadline')
        dept = get_object_or_404(Department, id=dept_id)
        
        if new_deadline_str:
            try:
                naive_datetime = datetime.strptime(new_deadline_str, '%Y-%m-%dT%H:%M')
                aware_datetime = timezone.make_aware(naive_datetime)
                dept.deadline = aware_datetime
                dept.save()
                messages.success(request, f"{dept.name} এর ডেডলাইন আপডেট হয়েছে।")
            except ValueError:
                messages.error(request, "তারিখের ফরম্যাট সঠিক নয়।")
    return redirect('dashboard')

def update_status(request, paper_id):
      if request.method == 'POST':
        paper = get_object_or_404(ResearchPaper, id=paper_id)
        
        paper.status = request.POST.get('status') # Approved বা Rejected
        paper.teacher_review = request.POST.get('review_text') # টিচারের মন্তব্য
        paper.save()
        return redirect('dashboard')

# --- সাধারণ পেজসমূহ ---
def home_view(request):
    return render(request, 'home.html')

def about_view(request):
    return render(request, 'about.html')

def contact_view(request):
    return render(request, 'contact.html')