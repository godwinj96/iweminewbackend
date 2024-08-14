from django.conf import settings
from django.db import models

import uuid

from useraccount.models import User

# Create your models here.

import os

def get_paper_cover_path(instance, filename):
    # Return the path to save the cover page
    return os.path.join('uploads', 'papers', instance.name, 'cover', filename)

def get_paper_file_path(instance, filename):
    # Return the path to save the paper file
    return os.path.join('uploads', 'papers', instance.name, filename)


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
    


class Papers(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(primary_key=True, max_length=200)
    author = models.CharField(max_length=255)
    abstract = models.TextField(null=True, blank=True)
    cover_page = models.ImageField(upload_to=get_paper_cover_path, null=True, blank=True)
    type = models.ForeignKey(Type, related_name='type', on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(Category, related_name='category', on_delete=models.SET_NULL, null=True, blank=True)
    subcategory = models.ForeignKey(SubCategory, related_name='subcategory', on_delete=models.SET_NULL, null=True, blank=True)
    year_published = models.CharField(max_length=255, null=True, blank=True)
    date_uploaded = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to=get_paper_file_path, null=True, blank=True)
    is_open_access = models.BooleanField(null=True, blank=True)
    is_approved = models.BooleanField(null=True, blank=True)
    citations = models.IntegerField(null=True, blank=True)
    references = models.TextField(null=True, blank=True)
    comments = models.TextField(null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    resource_id = models.CharField(max_length=255, null=True, blank=True)
    # new_price = models.IntegerField(null=True, blank=True)

    def cover_url(self):
        return f"{settings.WEBSITE_URL}{self.cover_page.url}"
    
    def __str__(self):
        return self.name
