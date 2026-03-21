from django.db import models
from django.contrib.auth.models import User

class ResearchPaper(models.Model):
    reviewer_feedback = models.TextField(null=True, blank=True)
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='reviewed_papers')
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    

    title = models.CharField(max_length=255)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=100)
    file = models.FileField(upload_to='papers/')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    plagiarism_score = models.FloatField(default=0.0) 
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
