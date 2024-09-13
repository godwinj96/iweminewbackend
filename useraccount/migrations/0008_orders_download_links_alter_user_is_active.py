# Generated by Django 5.0.7 on 2024-09-13 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('useraccount', '0007_orders'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='download_links',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
