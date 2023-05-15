import random
from django.conf import settings
from django.core.mail import send_mail
from celery import shared_task

# @shared_task(name="generate_otp")
def generate_otp():
    """
    Generate a 5-digit random OTP code.
    """
    return random.randint(10000, 99999)

# @shared_task(name="send_otp_email")
def send_otp_email(email, otp_code):
    """
    Send an email with the OTP code to the user's email address.
    """
    subject = 'Your OTP Code'
    message = f'Your OTP code is {otp_code}.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
