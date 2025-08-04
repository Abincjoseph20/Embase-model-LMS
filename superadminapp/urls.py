from django.urls import path
from .import views

urlpatterns = [
    path('', views.base_view, name='base_view'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    path('admin_dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('superadmin_dashboard/', views.superadmin_dasboard_view, name='superadmin_dashboard'),
    path('student_dashboard/', views.student_dashboard_view, name='student_dashboard'),
    path('teacher_dashboard/', views.teacher_dashboard_view, name='teacher_dashboard'),
    path('parent_dashboard/', views.parent_dashboard_view, name='parent_dashboard'),
    path('guest_dashboard/', views.guest_dashboard_view, name='guest_dashboard'),
    

    path('admin_register/', views.admin_register_view, name='admin_register'),
    
]
