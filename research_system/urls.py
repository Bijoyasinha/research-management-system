from django.contrib import admin
from django.urls import path
from core import views 

urlpatterns = [

    path('', views.login_view, name='login'), 
    
    path('admin/', admin.site.urls),
    path('upload/', views.upload_paper, name='upload_paper'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('review/<int:paper_id>/', views.review_paper, name='review_paper'),
    
]
