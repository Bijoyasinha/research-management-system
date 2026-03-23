from django.shortcuts import render, redirect
from .models import ResearchPaper
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required



def upload_paper(request):
    if request.method == "POST":
        title = request.POST.get('title')
        dept = request.POST.get('department')
        pdf_file = request.FILES.get('paper_file')

    
        ResearchPaper.objects.create(
            title=title,
            department=dept,
            file=pdf_file,
            student=request.user 
        )
        return redirect('dashboard')

    return render(request, 'upload.html')
def dashboard(request):
    papers = ResearchPaper.objects.all().order_by('department')
    return render(request, 'dashboard.html', {'papers': papers})
def review_paper(request, paper_id):
    paper = ResearchPaper.objects.get(id=paper_id)
    
    if request.method == "POST":
        status = request.POST.get('status')
        feedback = request.POST.get('feedback')
        
        paper.status = status
        paper.reviewer_feedback = feedback
        paper.save()
        return redirect('dashboard')
        
    return render(request, 'review_paper.html', {'paper': paper})


def login_view(request):
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        
        
        user = authenticate(request, username=u, password=p) 
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
        
            return render(request, 'login.html', {'error': 'Invalid username or password'})
            
    return render(request, 'login.html')
def dashboard(request):

    papers = ResearchPaper.objects.all().order_by('-submitted_at') 
    return render(request, 'dashboard.html', {'papers': papers})