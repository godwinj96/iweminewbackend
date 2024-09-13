from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from allauth.account.models import EmailAddress

@receiver(post_save, sender=User)
def send_confirmation_email(sender, instance, created, **kwargs):
    if created:
        email_address = EmailAddress.objects.create(
            user=instance,
            email=instance.email,
            verified=False,
            primary=True
        )
        print(f"signal received: {instance}")
        email_address.send_confirmation()


from django.dispatch import receiver
from allauth.account.signals import email_confirmed
from django.contrib.auth import get_user_model

# Get the custom user model
User = get_user_model()

@receiver(email_confirmed)
def activate_user_on_email_confirmation(request, email_address, **kwargs):
    user = email_address.user
    user.is_active = True
    user.save()
    print(f"User {user.email} has been activated")  # Debug print

