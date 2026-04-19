from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_view, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'), 
    path('signup/', views.signup_view, name='register'),
     
    path('logout/', views.logout_view, name='logout'),
    path('upload/', views.upload_paper, name='upload_paper'),
    path('review-paper/<int:paper_id>/', views.review_paper, name='review_paper'),
    path('delete-paper/<int:paper_id>/', views.delete_paper, name='delete_paper'), 
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('update-deadline/<int:dept_id>/', views.update_deadline, name='update_deadline'),
    path('signup/', views.signup_view, name='signup'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)