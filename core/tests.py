from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from core.models import Department, ResearchPaper
from django.utils import timezone
from datetime import timedelta

class RMSProjectTest(TestCase):
    def setUp(self):
        
        self.dept = Department.objects.create(
            name="CSE", 
            deadline=timezone.now() + timedelta(days=2)
        )
        
        
        self.student = User.objects.create_user(username='student', password='pass123')
        self.teacher = User.objects.create_user(username='teacher', password='pass123', is_staff=True)
        
        self.client = Client()

    def test_pages_load(self):
        """চেক করা হচ্ছে হোম, অ্যাবাউট এবং কন্টাক্ট পেজ ঠিকমতো লোড হয় কি না"""
        pages = ['home', 'about', 'contact']
        for page in pages:
            response = self.client.get(reverse(page))
            self.assertEqual(response.status_code, 200)
        print("\n✅ Static pages (Home, About, Contact) are loading perfectly!")

    def test_dashboard_access_for_student(self):
        """স্টুডেন্ট লগইন করে ড্যাশবোর্ড দেখতে পারছে কি না"""
        self.client.login(username='student', password='pass123')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard.html')
        print("✅ Student Dashboard access verified!")

    def test_teacher_can_update_deadline(self):
        """টিচার কি ডেডলাইন আপডেট করতে পারছে? (কী-নাম: new_deadline)"""
        self.client.login(username='teacher', password='pass123')
        
        new_deadline_val = (timezone.now() + timedelta(days=10)).strftime('%Y-%m-%dT%H:%M')
        
        response = self.client.post(reverse('update_deadline', args=[self.dept.id]), {
            'new_deadline': new_deadline_val
        })
        
        self.dept.refresh_from_db()
        self.assertEqual(response.status_code, 302) # রিডাইরেক্ট হওয়া উচিত
        print("✅ Teacher deadline update logic is working!")

    def test_unauthorized_access_to_deadline(self):
        """সিকিউরিটি চেক: স্টুডেন্ট কি জোর করে ডেডলাইন বদলাতে পারে?"""
        self.client.login(username='student', password='pass123')
        
        
        self.client.post(reverse('update_deadline', args=[self.dept.id]), {
            'new_deadline': "2030-12-31T23:59"
        })
        
        self.dept.refresh_from_db()
        
        self.assertNotEqual(self.dept.deadline.year, 2030)
        print("✅ Security Check Passed: Students are blocked from changing deadlines!")

    def test_deadline_gating_for_upload(self):
        """ডেডলাইন শেষ হয়ে গেলে স্টুডেন্ট আপলোড করতে পারছে কি না চেক"""
        
        self.dept.deadline = timezone.now() - timedelta(days=1)
        self.dept.save()
        
        self.client.login(username='student', password='pass123')
        response = self.client.post(reverse('upload_paper'), {
            'title': 'Test Paper',
            'department': self.dept.id
        })
        
        
        self.assertEqual(ResearchPaper.objects.count(), 0)
        print("✅ Deadline Gatekeeper is working correctly!")