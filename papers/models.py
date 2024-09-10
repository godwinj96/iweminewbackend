from django.conf import settings
from django.db import models
import os
import uuid
import re

from useraccount.models import User

# Create your models here.



MAX_PATH_LENGTH = 255  # Maximum path length on Windows


def sanitize_filename(name):
    """
    Remove or replace invalid characters from the directory name.
    """
    # Replace invalid characters with underscores
    sanitized_name = re.sub(r'[<>:"/\\|?*]', '_', name)
    return sanitized_name

def ensure_directory_exists(directory):
    """
    Ensure that the directory exists. If not, create it.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)

def get_truncated_filename(directory, filename, max_length):
    """
    Truncates the entire path (directory + filename) if it exceeds max_length.
    """
    full_path = os.path.join(directory, filename)
    
    # If the full path is too long, start truncating
    if len(full_path) > max_length:
        ext = os.path.splitext(filename)[-1]  # Get the file extension
        
        # Truncate the filename first
        filename_length = max_length - len(directory) - 1  # account for separator
        short_filename = f"{uuid.uuid4().hex[:10]}{ext}"
        
        # If filename is still too long, truncate directory names too
        while len(full_path) > max_length:
            directory_parts = directory.split(os.sep)
            if len(directory_parts) > 1:
                # Shorten the deepest directory
                directory_parts[-1] = directory_parts[-1][:10]
                directory = os.sep.join(directory_parts)
                full_path = os.path.join(directory, short_filename)
            else:
                break  # Can't shorten anymore
    
    print(f"Final truncated path: {full_path}")
    return full_path


def get_safe_directory_name(name, max_length=50):
    """
    Shortens and sanitizes the directory name if it's too long or contains invalid characters.
    """
    # Sanitize the name to remove or replace invalid characters
    sanitized_name = sanitize_filename(name)
    
    # Shorten the sanitized name if it's too long
    if len(sanitized_name) > max_length:
        # Generate a shortened name based on the first 40 characters and a UUID
        return f"{sanitized_name[:40]}_{uuid.uuid4().hex[:8]}"
    return sanitized_name


def get_paper_cover_path(instance, filename):
    # Shorten the instance name for the directory if it's too long
    safe_name = get_safe_directory_name(instance.name)
    
    # Define the directory to save the cover image
    directory = os.path.join('uploads', 'papers', safe_name, 'cover')
    
    # Ensure the directory exists
    ensure_directory_exists(directory)
    
    # Check the full path length and truncate if necessary
    return get_truncated_filename(directory, filename, MAX_PATH_LENGTH)


def get_paper_file_path(instance, filename):
    # Shorten the instance name for the directory if it's too long
    safe_name = get_safe_directory_name(instance.name)
    
    # Define the directory to save the paper file
    directory = os.path.join('uploads', 'papers', safe_name)
    
    # Ensure the directory exists
    ensure_directory_exists(directory)
    
    # Check the full path length and truncate if necessary
    return get_truncated_filename(directory, filename, MAX_PATH_LENGTH)


class Type(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField( max_length=200, unique=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField( max_length=200, unique=True)
    type = models.ManyToManyField(Type, blank=True)

    def __str__(self):
        return self.name
    

class SubCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField( max_length=200, unique=True)
    type = models.ManyToManyField(Type, blank=True)
    category = models.ManyToManyField(Category, blank=True)

    def __str__(self):
        return self.name


class Comments(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, blank=True)
    posted_by = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    content = models.TextField(null=True, blank=True)


class Papers(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(primary_key=True, max_length=500)
    author = models.CharField(max_length=255)
    abstract = models.TextField(null=True, blank=True)
    cover_page = models.ImageField(max_length=450, upload_to=get_paper_cover_path, null=True, blank=True)
    type = models.ForeignKey(Type, related_name='type', on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(Category, related_name='category', on_delete=models.SET_NULL, null=True, blank=True)
    subcategory = models.ForeignKey(SubCategory, related_name='subcategory', on_delete=models.SET_NULL, null=True, blank=True)
    year_published = models.CharField(max_length=255, null=True, blank=True)
    date_uploaded = models.DateTimeField(auto_now_add=True)
    file = models.FileField(max_length=450, upload_to=get_paper_file_path, null=True, blank=True)
    is_open_access = models.BooleanField(null=True, blank=True)
    is_approved = models.BooleanField(null=True, blank=True)
    citations = models.IntegerField(null=True, blank=True)
    references = models.TextField(null=True, blank=True)
    comments = models.ForeignKey(Comments, related_name='type', on_delete=models.SET_NULL, null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    resource_id = models.CharField(max_length=255, null=True, blank=True)
    # new_price = models.IntegerField(null=True, blank=True)

    def cover_url(self):
        return f"{settings.WEBSITE_URL}{self.cover_page.url}"
    
    def __str__(self):
        return self.name
