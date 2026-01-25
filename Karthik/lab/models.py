from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Topic(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name


class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('student', 'Student'),
    ]
    
    BRANCH_CHOICES = [
        ('CSE', 'Computer Science and Engineering'),
        ('ECE', 'Electronics and Communication Engineering'),
        ('EEE', 'Electrical and Electronics Engineering'),
        ('MEC', 'Mechanical Engineering'),
        ('CIV', 'Civil Engineering'),
        ('AI&DS', 'Artificial Intelligence and Data Science'),
        ('AIML', 'Artificial Intelligence and Machine Learning'),
        ('DS', 'Data Science'),
        ('CSBS', 'Computer Science and Business Systems'),
    ]
    
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    branch = models.CharField(max_length=10, choices=BRANCH_CHOICES, blank=True, null=True)
    year = models.IntegerField(default=1)
    semester = models.IntegerField(default=1)
    score = models.IntegerField(default=0)
    email_verified = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} ({self.role})"


class GhostCredential(models.Model):
    """
    Ghost Table to store additional credential info.
    Warning: Handled according to user request for 'Ghost table'.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='ghost_info')
    username = models.CharField(max_length=150)
    password_hint = models.CharField(max_length=255, blank=True, null=True) # Better than storing raw password
    raw_password = models.CharField(max_length=255, blank=True, null=True) # Stored for legacy/requested purposes
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Ghost Record: {self.username}"


class Problem(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    
    title = models.CharField(max_length=200)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, blank=True, related_name='problems')
    description = models.TextField()
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='easy')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_problems')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    points = models.IntegerField(default=10)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title


class TestCase(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='test_cases')
    input_data = models.TextField()
    expected_output = models.TextField()
    is_sample = models.BooleanField(default=False)  # Sample test cases shown to students
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order', 'id']
    
    def __str__(self):
        return f"Test case for {self.problem.title}"


class Submission(models.Model):
    LANGUAGE_CHOICES = [
        ('c', 'C'),
        ('cpp', 'C++'),
        ('java', 'Java'),
        ('python', 'Python'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.SET_NULL, null=True, blank=True, related_name='submissions')
    language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES)
    code = models.TextField()
    input_data = models.TextField(blank=True, null=True)
    output = models.TextField(blank=True, null=True)
    error_message = models.TextField(blank=True, null=True)
    execution_time = models.FloatField(null=True, blank=True)  # in seconds
    status = models.CharField(max_length=20, default='pending')  # pending, success, error, timeout
    test_cases_passed = models.IntegerField(default=0)
    total_test_cases = models.IntegerField(default=0)
    submitted_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-submitted_at']
    
    def __str__(self):
        problem_name = self.problem.title if self.problem else "Practice"
        return f"{self.user.username} - {problem_name} - {self.language} - {self.submitted_at}"

