from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_welcome_email_task(user_email):
    subject = 'Welcome to TaskForge!'
    message = 'This is a test email sent to you!'
    
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user_email],
        fail_silently=False,
    )
    return f"Real email sent to {user_email}"