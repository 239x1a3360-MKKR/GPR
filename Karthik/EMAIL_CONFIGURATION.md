# Email Configuration Guide

## Overview

The Virtual Lab system sends verification emails to users when they register. This guide explains how to configure email settings.

## Email Backend Options

### Option 1: Gmail SMTP (Recommended for Testing)

1. **Enable 2-Factor Authentication** on your Gmail account
2. **Generate an App Password**:
   - Go to Google Account → Security → 2-Step Verification → App passwords
   - Generate a password for "Mail"
   - Copy the 16-character password

3. **Set Environment Variables** (Windows PowerShell):
```powershell
$env:EMAIL_HOST_USER = "your.email@gmail.com"
$env:EMAIL_HOST_PASSWORD = "your-app-password"
$env:DEFAULT_FROM_EMAIL = "your.email@gmail.com"
```

4. **Or set in settings.py directly** (not recommended for production):
```python
EMAIL_HOST_USER = 'your.email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
DEFAULT_FROM_EMAIL = 'your.email@gmail.com'
```

### Option 2: Console Backend (Development/Testing)

For development, you can use the console backend to see emails in the terminal:

In `virtuallab/settings.py`, uncomment:
```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

This will print emails to the console instead of sending them.

### Option 3: SMTP Server (Production)

For production, use your organization's SMTP server:

```python
EMAIL_HOST = 'smtp.gprec.ac.in'  # Your SMTP server
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'noreply@gprec.ac.in'
EMAIL_HOST_PASSWORD = 'your-password'
DEFAULT_FROM_EMAIL = 'noreply@gprec.ac.in'
```

## Configuration Steps

### Step 1: Update Settings

Edit `virtuallab/settings.py` and configure:

```python
EMAIL_HOST = 'smtp.gmail.com'  # or your SMTP server
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
DEFAULT_FROM_EMAIL = 'your-email@gmail.com'
```

### Step 2: Test Email Configuration

Run Django shell to test:

```powershell
python manage.py shell
```

Then in the shell:
```python
from django.core.mail import send_mail
send_mail(
    'Test Email',
    'This is a test email.',
    'your-email@gmail.com',
    ['recipient@example.com'],
    fail_silently=False,
)
```

### Step 3: Restart Server

After configuring email, restart the Django server:

```powershell
python manage.py runserver
```

## Environment Variables (Recommended)

For security, use environment variables instead of hardcoding:

### Windows PowerShell:
```powershell
$env:EMAIL_HOST_USER = "your.email@gmail.com"
$env:EMAIL_HOST_PASSWORD = "your-app-password"
$env:DEFAULT_FROM_EMAIL = "your.email@gmail.com"
```

### Windows CMD:
```cmd
set EMAIL_HOST_USER=your.email@gmail.com
set EMAIL_HOST_PASSWORD=your-app-password
set DEFAULT_FROM_EMAIL=your.email@gmail.com
```

### Linux/macOS:
```bash
export EMAIL_HOST_USER="your.email@gmail.com"
export EMAIL_HOST_PASSWORD="your-app-password"
export DEFAULT_FROM_EMAIL="your.email@gmail.com"
```

## Troubleshooting

### Email Not Sending

1. **Check SMTP Settings**: Verify host, port, and TLS settings
2. **Check Credentials**: Ensure username and password are correct
3. **Check Firewall**: Ensure port 587 (or 465 for SSL) is not blocked
4. **Check Gmail App Password**: Make sure you're using an app password, not your regular password
5. **Check Spam Folder**: Emails might be going to spam

### Gmail Specific Issues

- **"Less secure app access"**: Gmail no longer supports this. Use App Passwords instead.
- **"Authentication failed"**: Check that you're using an App Password, not your regular password.
- **"Connection refused"**: Check firewall settings and ensure port 587 is open.

### Testing Without Sending Emails

For development, use console backend:

```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

This will print emails to the console instead of sending them.

## Email Template

The verification email uses a template located at:
`templates/lab/emails/verification_email.html`

You can customize this template to match your branding.

## Security Notes

1. **Never commit passwords to version control**
2. **Use environment variables for sensitive data**
3. **Use App Passwords for Gmail, not regular passwords**
4. **In production, use your organization's SMTP server**
5. **Consider using email services like SendGrid, Mailgun, or AWS SES for production**

## Current Configuration

The system is configured to:
- Send HTML emails with a professional template
- Include verification links
- Handle email sending failures gracefully
- Show verification links on screen if email sending fails (development mode)

