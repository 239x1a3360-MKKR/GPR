from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import path
from django.http import HttpResponse
from django.utils.safestring import mark_safe
from django.utils.html import format_html
import csv
import io
from .models import UserProfile, Submission, Problem, TestCase, Topic, GhostCredential

# Topic Management
@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']

# Ghost Credential Management
@admin.register(GhostCredential)
class GhostCredentialAdmin(admin.ModelAdmin):
    list_display = ['username', 'user', 'updated_at']
    search_fields = ['username', 'user__username']
    readonly_fields = ['updated_at']


from django.forms.models import BaseInlineFormSet

class UserProfileFormSet(BaseInlineFormSet):
    def save_new(self, form, commit=True):
        """Handle profile creation if signal already created it"""
        # Check if profile already exists (likely created by signal)
        existing = UserProfile.objects.filter(user=self.instance).first()
        if existing:
            # Merge form data into existing instance to avoid NOT NULL issues with created_at
            profile = form.save(commit=False)
            # Copy fields from form's instance to existing instance
            # We skip fields that shouldn't be overridden like PK and created_at
            for field in profile._meta.fields:
                if not field.primary_key and field.name != 'created_at':
                    setattr(existing, field.name, getattr(profile, field.name))
            if commit:
                existing.save()
            return existing
        
        return super().save_new(form, commit)

# Student Management
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    formset = UserProfileFormSet
    can_delete = False
    verbose_name_plural = 'Profile Info'
    fields = ['role', 'gender', 'branch', 'year', 'semester', 'score']

class GhostCredentialInline(admin.StackedInline):
    model = GhostCredential
    verbose_name_plural = 'Ghost Credentials (Audit)'
    fields = ['username', 'raw_password', 'updated_at']
    readonly_fields = ['username', 'raw_password', 'updated_at']
    can_delete = False
    extra = 0


class StudentAdmin(BaseUserAdmin):
    """Enhanced User admin for student management"""
    inlines = (UserProfileInline, GhostCredentialInline)
    list_display = ['username', 'email', 'get_branch', 'get_year', 'get_score', 'get_role', 'get_submission_count', 'date_joined', 'is_active']
    list_filter = ['is_active', 'is_staff', 'date_joined', 'userprofile__role', 'userprofile__branch', 'userprofile__year']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    actions = ['delete_selected_users']
    
    def get_role(self, obj):
        try:
            return obj.userprofile.role
        except:
            return 'N/A'
    get_role.short_description = 'Role'

    def get_branch(self, obj):
        try:
            return obj.userprofile.branch
        except:
            return 'N/A'
    get_branch.short_description = 'Branch'

    def get_year(self, obj):
        try:
            return obj.userprofile.year
        except:
            return 'N/A'
    get_year.short_description = 'Year'

    def get_score(self, obj):
        try:
            return obj.userprofile.score
        except:
            return 0
    get_score.short_description = 'Score'
    
    def get_submission_count(self, obj):
        count = Submission.objects.filter(user=obj).count()
        return format_html('<strong>{}</strong>', count)
    get_submission_count.short_description = 'Submissions'
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Filter to show students by default, but allow filtering
        if 'userprofile__role' in request.GET:
            return qs
        # Show all users but highlight students
        return qs
    
    def delete_model(self, request, obj):
        """Override delete to add safety checks"""
        # Prevent deleting yourself
        if obj == request.user:
            messages.error(request, 'You cannot delete your own account.')
            return
        
        # Prevent deleting superusers
        if obj.is_superuser and not request.user.is_superuser:
            messages.error(request, 'You cannot delete superuser accounts.')
            return
        
        # Show warning about related data
        submission_count = Submission.objects.filter(user=obj).count()
        if submission_count > 0:
            messages.warning(request, 
                f'Deleting user "{obj.username}" will also delete {submission_count} submission(s).')
        
        # Proceed with deletion
        super().delete_model(request, obj)
        messages.success(request, f'User "{obj.username}" has been deleted successfully.')
    
    def delete_queryset(self, request, queryset):
        """Override bulk delete to add safety checks"""
        # Prevent deleting yourself
        if request.user in queryset:
            messages.error(request, 'You cannot delete your own account.')
            queryset = queryset.exclude(pk=request.user.pk)
        
        # Prevent deleting superusers (unless current user is superuser)
        if not request.user.is_superuser:
            superusers = queryset.filter(is_superuser=True)
            if superusers.exists():
                messages.error(request, 
                    f'Cannot delete {superusers.count()} superuser account(s). Only superusers can delete other superusers.')
                queryset = queryset.exclude(is_superuser=True)
        
        # Count related data
        total_submissions = Submission.objects.filter(user__in=queryset).count()
        if total_submissions > 0:
            messages.warning(request, 
                f'Deleting {queryset.count()} user(s) will also delete {total_submissions} submission(s).')
        
        # Proceed with deletion
        deleted_count = queryset.count()
        super().delete_queryset(request, queryset)
        messages.success(request, f'{deleted_count} user(s) deleted successfully.')
    
    def delete_selected_users(self, request, queryset):
        """Custom action for deleting selected users"""
        self.delete_queryset(request, queryset)
    delete_selected_users.short_description = "Delete selected users"
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('import-user-csv/', self.admin_site.admin_view(self.import_user_csv_view), name='lab_user_import_csv'),
        ]
        return custom_urls + urls

    def import_user_csv_view(self, request):
        if request.method == 'POST':
            csv_file = request.FILES.get('csv_file')
            if not csv_file:
                messages.error(request, 'Please select a CSV file.')
                return redirect('admin:lab_user_import_csv')
            
            try:
                decoded_file = csv_file.read().decode('utf-8')
                io_string = io.StringIO(decoded_file)
                reader = csv.DictReader(io_string)
                
                imported_count = 0
                errors = []
                
                for row_num, row in enumerate(reader, start=2):
                    try:
                        username = row.get('username', '').strip()
                        email = row.get('email', '').strip()
                        password = row.get('password', '').strip()
                        branch = row.get('branch', '').strip()
                        year = row.get('year', '1').strip()
                        semester = row.get('semester', '1').strip()
                        gender = row.get('gender', 'Male').strip()
                        role = row.get('role', 'student').strip().lower()
                        
                        if not username or not email or not password:
                            errors.append(f"Row {row_num}: Missing username, email or password")
                            continue
                        
                        if User.objects.filter(username=username).exists():
                            errors.append(f"Row {row_num}: Username '{username}' already exists")
                            continue
                            
                        if User.objects.filter(email=email).exists():
                            errors.append(f"Row {row_num}: Email '{email}' already registered")
                            continue

                        # Create user
                        user = User.objects.create_user(
                            username=username, 
                            email=email, 
                            password=password
                        )
                        
                        # Update profile (created by signal)
                        profile = user.userprofile
                        profile.branch = branch
                        profile.year = int(year) if year.isdigit() else 1
                        profile.semester = int(semester) if semester.isdigit() else 1
                        profile.gender = gender
                        profile.role = role if role in ['admin', 'student'] else 'student'
                        profile.email_verified = True # Auto verify imported users
                        profile.save()
                        
                        imported_count += 1
                        
                    except Exception as e:
                        errors.append(f"Row {row_num}: {str(e)}")
                
                if imported_count > 0:
                    messages.success(request, f'Successfully imported {imported_count} user(s).')
                if errors:
                    for error in errors:
                        messages.warning(request, error)
                        
            except Exception as e:
                messages.error(request, f'Error importing CSV: {str(e)}')
            
            return redirect('admin:auth_user_changelist')
        
        context = {
            **self.admin_site.each_context(request),
            'opts': self.model._meta,
            'title': 'Import Users from CSV',
        }
        return render(request, 'admin/lab/user/import_csv.html', context)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['user_import_csv_url'] = 'admin:lab_user_import_csv'
        return super().changelist_view(request, extra_context=extra_context)


# Unregister default User admin and register custom one
admin.site.unregister(User)
admin.site.register(User, StudentAdmin)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'branch', 'year', 'score', 'role', 'email_verified', 'created_at']
    list_filter = ['role', 'branch', 'year', 'semester', 'email_verified', 'created_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at']
    actions = ['delete_selected_profiles']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'role', 'gender', 'email_verified')
        }),
        ('Academic Information', {
            'fields': ('branch', 'year', 'semester')
        }),
        ('Performance', {
            'fields': ('score',)
        }),
        ('Statistics', {
            'fields': ('created_at',)
        }),
    )
    
    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'
    
    def get_submission_count(self, obj):
        count = Submission.objects.filter(user=obj.user).count()
        return format_html('<strong>{}</strong>', count)
    get_submission_count.short_description = 'Submissions'
    
    def delete_model(self, request, obj):
        """Override delete to add safety checks"""
        # Prevent deleting your own profile
        if obj.user == request.user:
            messages.error(request, 'You cannot delete your own profile.')
            return
        
        # Prevent deleting admin profiles (unless current user is superuser)
        if obj.role == 'admin' and not request.user.is_superuser:
            messages.error(request, 'You cannot delete admin profiles.')
            return
        
        super().delete_model(request, obj)
        messages.success(request, f'Profile for "{obj.user.username}" has been deleted successfully.')
    
    def delete_queryset(self, request, queryset):
        """Override bulk delete to add safety checks"""
        # Prevent deleting your own profile
        if hasattr(request.user, 'userprofile') and request.user.userprofile in queryset:
            messages.error(request, 'You cannot delete your own profile.')
            queryset = queryset.exclude(user=request.user)
        
        # Prevent deleting admin profiles (unless current user is superuser)
        if not request.user.is_superuser:
            admin_profiles = queryset.filter(role='admin')
            if admin_profiles.exists():
                messages.error(request, 
                    f'Cannot delete {admin_profiles.count()} admin profile(s). Only superusers can delete admin profiles.')
                queryset = queryset.exclude(role='admin')
        
        deleted_count = queryset.count()
        super().delete_queryset(request, queryset)
        if deleted_count > 0:
            messages.success(request, f'{deleted_count} profile(s) deleted successfully.')
    
    def delete_selected_profiles(self, request, queryset):
        """Custom action for deleting selected profiles"""
        self.delete_queryset(request, queryset)
    delete_selected_profiles.short_description = "Delete selected profiles"


class SampleTestCaseInline(admin.TabularInline):
    """Inline for Sample Test Cases (Visible to Students)"""
    model = TestCase
    extra = 2
    fields = ['input_data', 'expected_output', 'order']
    verbose_name = "Sample Test Case (Visible to Students)"
    verbose_name_plural = "Sample Test Cases (Visible to Students)"
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(is_sample=True)
    
    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        formset.form.base_fields['input_data'].help_text = "Input data that students will see"
        formset.form.base_fields['expected_output'].help_text = "Expected output that students will see"
        return formset


class HiddenTestCaseInline(admin.TabularInline):
    """Inline for Hidden Test Cases (For Evaluation Only)"""
    model = TestCase
    extra = 3
    fields = ['input_data', 'expected_output', 'order']
    verbose_name = "Hidden Test Case (Evaluation Only)"
    verbose_name_plural = "Hidden Test Cases (Evaluation Only)"
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(is_sample=False)
    
    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        formset.form.base_fields['input_data'].help_text = "Input data for evaluation (students won't see this)"
        formset.form.base_fields['expected_output'].help_text = "Expected output for evaluation (must match exactly)"
        return formset


@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ['title', 'topic', 'difficulty', 'points', 'is_active', 'test_case_count', 'created_by', 'created_at']
    list_filter = ['topic', 'difficulty', 'is_active', 'created_at']
    search_fields = ['title', 'description']
    inlines = [SampleTestCaseInline, HiddenTestCaseInline]
    readonly_fields = ['created_at', 'updated_at', 'test_case_info']
    
    fieldsets = (
        ('Problem Statement', {
            'fields': ('title', 'topic', 'description', 'difficulty', 'points', 'is_active'),
            'description': 'Enter the problem title and detailed description that students will see.'
        }),
        ('Test Cases Summary', {
            'fields': ('test_case_info',),
            'description': 'Manage test cases in the sections below. Sample test cases are visible to students. Hidden test cases are used only for evaluation.'
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def test_case_count(self, obj):
        """Display total test cases count in list view"""
        if obj.pk:
            total = obj.test_cases.count()
            sample = obj.test_cases.filter(is_sample=True).count()
            hidden = total - sample
            return f"{total} (S:{sample}, H:{hidden})"
        return "-"
    test_case_count.short_description = "Test Cases"
    
    def test_case_info(self, obj):
        """Display test case information and instructions"""
        if obj.pk:
            total = obj.test_cases.count()
            sample = obj.test_cases.filter(is_sample=True).count()
            hidden = total - sample
            info = f"<div style='background: #e8f4f8; padding: 10px; border-left: 4px solid #417690; margin: 10px 0;'>"
            info += f"<strong>Current Test Cases:</strong> Total: {total} | Sample (visible): {sample} | Hidden (evaluation only): {hidden}"
            info += "</div>"
            info += "<p><strong>Instructions:</strong></p>"
            info += "<ul style='margin-left: 20px;'>"
            info += "<li><strong>Sample Test Cases:</strong> Check 'Is sample' - These are shown to students to help them understand the problem</li>"
            info += "<li><strong>Hidden Test Cases:</strong> Uncheck 'Is sample' - These are used only for evaluation and are not visible to students</li>"
            info += "<li>You can add multiple test cases of both types</li>"
            info += "</ul>"
            return mark_safe(info)
        info = (
            "<div style='background: #fff3cd; padding: 10px; border-left: 4px solid #ffc107; margin: 10px 0;'>"
            "<p><strong>Adding Test Cases:</strong></p>"
            "<ul style='margin-left: 20px;'>"
            "<li>Scroll down to the 'Test Cases' section below</li>"
            "<li>Fill in <strong>Input data</strong> and <strong>Expected output</strong> for each test case</li>"
            "<li>Check <strong>Is sample</strong> to show the test case to students (recommended for at least 1-2 test cases)</li>"
            "<li>Uncheck <strong>Is sample</strong> to create hidden test cases for evaluation (students won't see these)</li>"
            "<li>Use <strong>Order</strong> to control the sequence of test cases</li>"
            "</ul>"
            "</div>"
        )
        return mark_safe(info)
    test_case_info.short_description = "Test Cases Information"
    
    def save_model(self, request, obj, form, change):
        if not change:  # Only set created_by when creating new
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
    
    def save_formset(self, request, form, formset, change):
        """Override to set is_sample based on which inline was used"""
        instances = formset.save(commit=False)
        for instance in instances:
            # Determine which inline this came from based on the formset prefix
            if 'sampletestcase_set' in str(formset.prefix):
                instance.is_sample = True
            elif 'hiddentestcase_set' in str(formset.prefix):
                instance.is_sample = False
            instance.save()
        for obj in formset.deleted_objects:
            obj.delete()
        formset.save_m2m()
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('import-csv/', self.admin_site.admin_view(self.import_csv_view), name='lab_problem_import_csv'),
            path('<int:problem_id>/editor/', self.admin_site.admin_view(self.problem_editor_view), name='lab_problem_editor'),
        ]
        return custom_urls + urls
    
    def problem_editor_view(self, request, problem_id):
        """Dedicated problem editor view with separate test case sections"""
        try:
            problem = Problem.objects.get(id=problem_id)
        except Problem.DoesNotExist:
            messages.error(request, 'Problem not found.')
            return redirect('admin:lab_problem_changelist')
        
        sample_test_cases = problem.test_cases.filter(is_sample=True).order_by('order', 'id')
        hidden_test_cases = problem.test_cases.filter(is_sample=False).order_by('order', 'id')
        topics = Topic.objects.all()
        
        context = {
            **self.admin_site.each_context(request),
            'opts': self.model._meta,
            'problem': problem,
            'topics': topics,
            'sample_test_cases': sample_test_cases,
            'hidden_test_cases': hidden_test_cases,
            'title': f'Problem Editor: {problem.title}',
        }
        return render(request, 'admin/lab/problem/editor.html', context)
    
    def import_csv_view(self, request):
        if request.method == 'POST':
            csv_file = request.FILES.get('csv_file')
            if not csv_file:
                messages.error(request, 'Please select a CSV file.')
                return redirect('admin:lab_problem_import_csv')
            
            try:
                # Read CSV file
                decoded_file = csv_file.read().decode('utf-8')
                io_string = io.StringIO(decoded_file)
                reader = csv.DictReader(io_string)
                
                imported_count = 0
                errors = []
                
                for row_num, row in enumerate(reader, start=2):  # Start at 2 (1 is header)
                    try:
                        # Required fields: title, description
                        title = row.get('title', '').strip()
                        description = row.get('description', '').strip()
                        difficulty = row.get('difficulty', 'easy').strip().lower()
                        is_active = row.get('is_active', 'true').strip().lower() == 'true'
                        points = row.get('points', '10').strip()
                        topic_name = row.get('topic', '').strip()
                        
                        topic = None
                        if topic_name:
                            topic, _ = Topic.objects.get_or_create(name=topic_name)
                        
                        if not title or not description:
                            errors.append(f"Row {row_num}: Missing title or description")
                            continue
                        
                        # Create problem
                        problem = Problem.objects.create(
                            title=title,
                            description=description,
                            difficulty=difficulty if difficulty in ['easy', 'medium', 'hard'] else 'easy',
                            is_active=is_active,
                            points=int(points) if points.isdigit() else 10,
                            topic=topic,
                            created_by=request.user
                        )
                        
                        # Add test cases if provided
                        test_input = row.get('test_input', '').strip()
                        test_output = row.get('test_output', '').strip()
                        is_sample = row.get('is_sample', 'false').strip().lower() == 'true'
                        
                        if test_input and test_output:
                            TestCase.objects.create(
                                problem=problem,
                                input_data=test_input,
                                expected_output=test_output,
                                is_sample=is_sample,
                                order=0
                            )
                        
                        imported_count += 1
                        
                    except Exception as e:
                        errors.append(f"Row {row_num}: {str(e)}")
                
                if imported_count > 0:
                    messages.success(request, f'Successfully imported {imported_count} problem(s).')
                if errors:
                    for error in errors:
                        messages.warning(request, error)
                        
            except Exception as e:
                messages.error(request, f'Error importing CSV: {str(e)}')
            
            return redirect('admin:lab_problem_changelist')
        
        # GET request - show upload form
        context = {
            **self.admin_site.each_context(request),
            'opts': self.model._meta,
            'title': 'Import Problems from CSV',
        }
        return render(request, 'admin/lab/problem/import_csv.html', context)
    
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['import_csv_url'] = 'admin:lab_problem_import_csv'
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(TestCase)
class TestCaseAdmin(admin.ModelAdmin):
    list_display = ['problem', 'is_sample', 'order']
    list_filter = ['is_sample', 'problem']
    search_fields = ['problem__title']


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_branch', 'get_year', 'problem', 'language', 'status', 'submitted_at']
    list_filter = ['status', 'language', 'user__userprofile__branch', 'user__userprofile__year', 'submitted_at', 'problem']
    search_fields = ['user__username', 'code', 'problem__title']
    readonly_fields = ['submitted_at']

    def get_branch(self, obj):
        try:
            return obj.user.userprofile.branch
        except:
            return 'N/A'
    get_branch.short_description = 'Branch'

    def get_year(self, obj):
        try:
            return obj.user.userprofile.year
        except:
            return 'N/A'
    get_year.short_description = 'Year'
    
    fieldsets = (
        ('Submission Info', {
            'fields': ('user', 'problem', 'language', 'submitted_at', 'status', 'execution_time')
        }),
        ('Test Results', {
            'fields': ('test_cases_passed', 'total_test_cases')
        }),
        ('Code', {
            'fields': ('code', 'input_data')
        }),
        ('Results', {
            'fields': ('output', 'error_message')
        }),
    )

