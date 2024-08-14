from django.core.mail.utils import send_mail

send_mail(
    'Test Email',
    'This is a test email.',
    'your_email@gmail.com',
    ['recipient_email@example.com'],
    fail_silently=False,
)