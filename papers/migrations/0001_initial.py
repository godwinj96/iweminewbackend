# Generated by Django 5.0.7 on 2024-08-08 12:00

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('name', models.CharField(max_length=200, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('name', models.CharField(max_length=200, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('name', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('category', models.ManyToManyField(to='papers.category')),
                ('type', models.ManyToManyField(to='papers.type')),
            ],
        ),
        migrations.CreateModel(
            name='Papers',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('name', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('abstract', models.TextField(blank=True, null=True)),
                ('cover_page', models.ImageField(upload_to='uploads/covers')),
                ('year_published', models.DateField(blank=True, null=True)),
                ('date_uploaded', models.DateTimeField(auto_now_add=True)),
                ('is_open_access', models.BooleanField(blank=True, null=True)),
                ('is_approved', models.BooleanField(blank=True, null=True)),
                ('citations', models.IntegerField(blank=True, null=True)),
                ('references', models.TextField(blank=True, null=True)),
                ('comments', models.TextField(blank=True, null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='papers', to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='category', to='papers.category')),
                ('subcategory', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subcategory', to='papers.subcategory')),
                ('type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='type', to='papers.type')),
            ],
        ),
        migrations.AddField(
            model_name='category',
            name='type',
            field=models.ManyToManyField(to='papers.type'),
        ),
    ]
