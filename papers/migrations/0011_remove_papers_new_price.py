# Generated by Django 5.0.7 on 2024-08-14 11:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('papers', '0010_papers_new_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='papers',
            name='new_price',
        ),
    ]
