import uuid
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager

from django.db import models
from allauth.account.models import EmailAddress

# Create your models here.

class CustomUserManager(UserManager):
    def _create_user(self, name, email, password, **extra_fields):
        if not email:
            raise ValueError('You have not specified a valid email address')

        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)

        # Set the password
        user.set_password(password)

        # Save the user first to get a valid user ID
        user.save(using=self.db)
        
        # Create the EmailAddress and send confirmation
        email_address = EmailAddress.objects.create(user=user, email=user.email, primary=True)
        email_address.send_confirmation()
        
        print(email_address)  # Debug print
        print("Email confirmation sent")  # Debug print

        return user
    
    def create_user(self, name=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(name, email, password, **extra_fields)
    
    def create_superuser(self, name=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(name, email, password, **extra_fields)



class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, db_index=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    avatar = models.ImageField(upload_to='uploads/avatars', null=True, blank=True)
    education = models.CharField(max_length=255, null=True, blank=True)
    institution = models.CharField(max_length=255, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_publisher = models.BooleanField(default=False)

    date_joined = models.DateTimeField(auto_now_add=True, editable=False)
    last_login = models.DateTimeField(blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['name', ]



class Orders(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    paper = models.ForeignKey('papers.Papers', on_delete=models.CASCADE, related_name="orders") 
    download_links = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    time_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100)  # e.g., 'completed', 'pending', etc.

    def __str__(self):
        return f"{self.user.name}'s Order for {self.paper.name}"
