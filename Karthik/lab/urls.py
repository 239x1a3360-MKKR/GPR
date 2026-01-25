from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views

app_name = 'lab'

urlpatterns = [
    # Web views
    path('', views.index, name='index'),
    path('editor/', views.editor, name='editor'),
    path('login/', views.login_view, name='login'),
    path('profile-settings/', views.profile_settings, name='profile_settings'),
    # path('register/', views.register_view, name='register'), # Removed
    path('logout/', views.logout_view, name='logout'),
    path('verify-email/<str:token>/', views.verify_email_view, name='verify_email'),
    path('resend-verification/', views.resend_verification, name='resend_verification'),
    path('problems/', views.problems_list, name='problems_list'),
    path('problems/<int:problem_id>/', views.problem_detail, name='problem_detail'),
    
    # Password Reset
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(
             template_name='lab/password_reset.html',
             success_url=reverse_lazy('lab:password_reset_done'),
             email_template_name='lab/emails/password_reset_email.html',
             subject_template_name='lab/emails/password_reset_subject.txt'
         ), 
         name='password_reset'),
    
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(template_name='lab/password_reset_done.html'), 
         name='password_reset_done'),
    
    path('password-reset-confirm/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(
             template_name='lab/password_reset_confirm.html',
             success_url=reverse_lazy('lab:password_reset_complete')
         ), 
         name='password_reset_confirm'),
    
    path('password-reset-complete/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='lab/password_reset_complete.html'), 
         name='password_reset_complete'),

    # API endpoints
    path('execute/', views.execute_code, name='execute_code'),
    path('submissions/', views.get_submissions, name='submissions'),
    path('submissions/<int:submission_id>/', views.get_submission_detail, name='submission_detail'),
]

