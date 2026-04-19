from django.db import models
from django.contrib.auth.models import User

class Department(models.Model):
    name = models.CharField(max_length=100)
    deadline = models.DateTimeField(null=True, blank=True)
    def __str__(self): return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self): return f"{self.user.username} - {self.department}"


STATUS_CHOICES = [ 
     
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
class ResearchPaper(models.Model):
 title = models.CharField(max_length=255)
 student = models.ForeignKey(User, on_delete=models.CASCADE)
 department = models.ForeignKey(Department, on_delete=models.CASCADE)
 file = models.FileField(upload_to='papers/')
 status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
 teacher_review = models.TextField(null=True, blank=True)
 plagiarism_score = models.FloatField(default=0.0)
 submitted_at = models.DateTimeField(auto_now_add=True)

 def __str__(self):
        return self.title