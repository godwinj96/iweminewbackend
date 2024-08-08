from django.conf import settings
from django.db import models

import uuid

from useraccount.models import User

# Create your models here.

class Type(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    type = models.ManyToManyField(Type)

    def __str__(self):
        return self.name
    

class SubCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    type = models.ManyToManyField(Type)
    category = models.ManyToManyField(Category)

    def __str__(self):
        return self.name
    


class Papers(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    author = models.ForeignKey(User, related_name='papers', on_delete=models.CASCADE)
    abstract =  models.TextField(null=True, blank=True)
    cover_page = models.ImageField(upload_to='uploads/covers')
    type = models.ForeignKey(Type, related_name='type', on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, related_name='category', on_delete=models.SET_NULL, null=True)
    subcategory = models.ForeignKey(SubCategory, related_name='subcategory', on_delete=models.SET_NULL, null=True)
    year_published = models.DateField()
    date_uploaded = models.DateTimeField(auto_now_add=True,)
    is_open_access = models.BooleanField(null=True, blank=True) 
    is_approved = models.BooleanField(null=True, blank=True)
    citations = models.IntegerField(null=True, blank=True)
    references = models.TextField(null=True, blank=True)
    comments = models.TextField(null=True, blank=True)
    # file = models.FileField()

    def cover_url(self):
        return f"{settings.WEBSITE_URL}{self.image.url}"
    
    def __str__(self):
        return self.name
    
