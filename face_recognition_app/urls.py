# face_recognition_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Vistas principales
    path('', views.login_view, name='login'),
    path('register/', views.register_page, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('train/', views.train_model_view, name='train_model'),
    path('recognition/', views.recognition_view, name='recognition'),
    path('logout/', views.logout_view, name='logout'),
    
    # APIs para reconocimiento
    path('api/recognize-login/', views.api_recognize_login, name='api_recognize_login'),
    path('api/recognize-realtime/', views.api_recognize_realtime, name='api_recognize_realtime'),
    path('api/process-frame/', views.process_frame, name='process_frame'),
    path('api/register-complete/', views.api_register_complete, name='api_register_complete'),
    
    # APIs para dashboard
    path('api/dashboard-stats/', views.api_dashboard_stats, name='api_dashboard_stats'),
    path('api/persons-list/', views.api_persons_list, name='api_persons_list'),
    path('api/delete-person/', views.api_delete_person, name='api_delete_person'),
]